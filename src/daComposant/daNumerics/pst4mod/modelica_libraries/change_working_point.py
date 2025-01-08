# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2025 EDF R&D
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA

###############################################################################
#                            LIBRARIES IMPORT                                 #
###############################################################################
import logging
from copy import copy
from os import path,mkdir,remove
from shutil import copytree,rmtree

from .automatic_simulation import Automatic_Simulation
from .functions import get_cur_time
###############################################################################
#                     CLASS Working_Point_Modification                        #
###############################################################################

class Working_Point_Modification(object):
    """
    Class Working_Point_Modification aims at making it easier to make a Modelica model
    converge when one (or several) of its variables has (have) to be changed. Depending on the impact of
    the variable, changing the value by a few percent can indeed be very hard.

    Generally, when the initial state is too far from the reference one for Dymola
    to be able to converge towards the solution with its reference initialisation
    script, it is possible to give ramps to Dymola (or other software) to help
    it converging. Yet, if the model contains inverted values that should be
    inverted only in a stationary state, giving ramps to help the model
    converging does not work (the parameters that have been calculated at t=0
    would be wrong).

    Class Working_Point_Modification aims at helping solving this difficulty.
    It can also be used for a model which does not contain any inverted values, in
    case the modeler does not want to change his model so that the parameters could
    be given as ramps.

    It runs several iterations, converging iteratively from the reference initial
    state to the desired state.

    Dymola must be able to simulate the Modelica model in the reference state.

    Required material:
        main_dir            String
                            Path of the directory in which directories will be created
        simu_material_dir   String
                            Name of the subdirectory of main_dir which contains all the required material to run a simulation (dymosim.exe, dsin.txt, .dll files, files that are necesssary to create an initialization script)
        around_simulation0  Object of type Around_Simulation (class defined in around_simulation)
                            Contains the material to create an initialization script
        dict_var_to_fix     Dictionary
                            Contains the names of the variables that must be imposed to
                            different values between reference state and the target state,
                            and the values they must be given at each state between the
                            reference and target states (information contained by a function)
    The other arguments are optional, but more information can be found in the attributes getters

    New features introduced 02/2019:
    - the possibility of using a dymosim situated in a given folder (featured introduced in automatic_simulation.py)
    is introduced
    - the previous use of this module should remain unchanged compared to previous version
    - possibility of running this script in Linux (not tested)
    """
    def __init__(self,main_dir,simu_material_dir,
                 around_simulation0,dict_var_to_fix,
                 dymosim_path=None,
                 simu_dir='SIMUS_DIR',store_res_dir='Working_point_change',
                 linux=False,
                 timeout=60,cur_step=1.,nit_max=20,var_to_follow_path='var_to_follow.csv',
                 gen_scripts_ini=False,pause=5.,min_step_val = 0.01,check_inputs=[]):

        self.__main_dir = path.abspath(main_dir)
        self.__simu_material_dir = simu_material_dir

        self.__store_res_dir = store_res_dir
        around_simulation0.verbose = False #To avoid repetitive messages
        self.__around_simulation0 = around_simulation0
        self.__dict_var_to_fix = dict_var_to_fix
        self.__simu_dir = simu_dir
        self.__linux = linux
        self.__timeout = timeout
        self.__cur_step = cur_step
        self.__nit_max = nit_max
        self.__var_to_follow_path = var_to_follow_path
        self.__gen_scripts_ini = gen_scripts_ini
        self.__pause = pause
        self.__min_step_val = min_step_val

        self.__around_simulation = None
        self.__dict_inputs = {}
        self.__val = 0.
        self.__ref_success_code = 99
        self.__success_code = 99
        self.__nit = 0
        self.__converging_val = None
        self.__list_inputs = []
        self.__res = None

        if dymosim_path is None:
            self.__dymosim_path = None
        elif path.isdir(dymosim_path):
            if self.linux:
                self.__dymosim_path = path.join(path.abspath(dymosim_path),'dymosim')
            else:
                self.__dymosim_path = path.join(path.abspath(dymosim_path),'dymosim.exe')
        elif path.isfile(dymosim_path):
            self.__dymosim_path = dymosim_path
        else:
            raise ValueError('Model file or directory not found using %s'%str(dymosim_path))

        if check_inputs is True:
            self.__check_inputs = dict_var_to_fix.keys()
        else:
            self.__check_inputs = check_inputs

###############################################################################
#                                  GETTERS                                    #
###############################################################################
    @property
    def main_dir(self):
        """
        Type: String
        Path of the main directory - relative path from the path where the script
        is executed or absolute path.
        """
        return self.__main_dir

    @property
    def check_inputs(self):
        """
        Variable used to select inputs that have to be checked: set value vs. used
        Possible values:
         - True : all variables in dict_inputs are checked
         - List of variables name to be checked
        """
        return self.__check_inputs

    @property
    def simu_material_dir(self):
        """
        Type: String
        Path of the main directory which contains all the files that are required to
        simulate the model. These files will be copied and this directory will
        not be changed - relative path from main_dir
        """
        return self.__simu_material_dir

    @property
    def store_res_dir(self):
        """
        Type: String
        Name of the directory where the simulation results will be stored
        """
        return self.__store_res_dir

    @property
    def around_simulation0(self):
        """
        Type: Around_Simulation
        around_simulation0 must contain enough information to create a script that
        can make the simulation converge in the reference state
        More information about object of type Around_Simulation in file
        around_simulation.py.
        """
        return self.__around_simulation0

    @property
    def dict_var_to_fix(self):
        """
        Type: Dictionary
        Dictionary which associates
            key     (Modelica) name of the variable whose value must be fixed
            value   Function which returns the value of variable key (0-> ref_val,
                    1 -> target_val)
        dict_var_to_fix can be generated using class Dict_Var_To_Fix.
        """
        return self.__dict_var_to_fix

    @property
    def simu_dir(self):
        """
        Type: String
        Path of the directory in which all the simulations will be run
        """
        return self.__simu_dir

    def dymosim_path(self):
        """
        Path of the directory that contains the dymosim.exe (or equivalent) file,
        can be different of simu_dir
        """
        return self.__dymosim_path

    @property
    def linux(self):
        """
        If the script has to be run on Linux, this attribute should be setted to True.
        On Linux, the exe file is indeed named "dymosim" instead of "dymosim.exe".
        """
        return self.__linux

    @property
    def timeout(self):
        """
        Type: Integer
        If a simulation has not converged after timeout, the siumlation is stopped.
        """
        return self.__timeout

    @property
    def cur_step(self):
        """
        Type: Float
        Current step (0: reference value;1: target value)
        -> with cur_step=0.5,the simulation will try to converge in 2 steps.
        """
        return self.__cur_step

    @property
    def nit_max(self):
        """
        Type: Integer
        Maximum number of iterations
        """
        return self.__nit_max

    @property
    def var_to_follow_path(self):
        """
        Type: String
        Path of the file containing the values of the interesting
        variables which are saved each time a simulation converges
        """
        return self.__var_to_follow_path

    @property
    def gen_scripts_ini(self):
        """
        Type: Boolean
        If True, each time a simulation has converged, the associated
        initialization script is generated.
        """
        return self.__gen_scripts_ini

    @property
    def pause(self):
        """
        Type: Float
        Number of seconds that are given to the system to copy the files
        I could try to replace it by calling a subprocess and waiting for the end
        of this subprocess
        """
        return self.__pause

    @property
    def around_simulation(self):
        """
        Type: Around_Simulation
        around_simulation contains enough information to generated initialization
        scripts.

        More information about object of type Around_Simulation in file
        around_simulation.py.
        """
        return self.__around_simulation

    @property
    def dict_inputs(self):
        """
        Type: Dictionary
        Dictionary associating to each variable whose value has to be given to
        dsin.txt (variables whose values must be fixed + iteration variables) its value.
        """
        return self.__dict_inputs

    @property
    def val(self):
        """
        Type: float
        Caracterise the distance from the reference state and to the target state.
        0. in the reference state
        1. in the final state when the working point change has reached its target
        """
        return self.__val

    @property
    def success_code(self):
        """
        Type: Integer
        If a simulation converges, this attribute is setted to 0
        If a simulation fails to initialize, this attribute is setted to 1
        If a simulation fails after the initialization, this attribute is setted to 2
        If a simulation does not fail but does not converge either, this attribute is setted to 3
        Default value: 99
        """
        return self.__success_code

    @property
    def ref_success_code(self):
        """
        Type: Integer
        Before trying to reach the target state, the user should try to simulate
        the reference state.
        If this "reference simulation" converges, this attribute is setted to 0.
        If this "reference simulation" fails to initialize, this attribute is setted to 1
        If this "reference simulation" fails after the initialization, this attribute is setted to 2
        If this "reference simulation" does not fail but does not converge either, this attribute is setted to 3
        Default value: 99

        If the value of this attribute is 1, no further calculation will be made.
        """
        return self.__ref_success_code

    @property
    def nit(self):
        """
        Type: Integer
        Number of simulation that have been run
        """
        return self.__nit

    @property
    def converging_val(self):
        """
        Type: Float
        Highest value for which the simulation has converged
        0 -> reference state
        1 -> target state
        """
        return self.__converging_val

    @property
    def min_step_val(self):
        """
        Type: Float
        Mininum allowed value for the step. If the script tries to use a value
        lower than min_step_val, it will stop.
        """
        return self.__min_step_val

    @property
    def list_inputs(self):
        """
        Type: List
        List of the input variable (Modelica) names
        """
        return self.__list_inputs

    @property
    def res(self):
        """
        Type: Dictionary
        It is a dictionary containing the values of self.list_inputs at the end
        of a simulation (the values of the iteration variables in this attribute
        will therefore be injected in the next simulation)
        """
        return self.__res
###############################################################################
#                                  SETTERS                                    #
###############################################################################

    def set_success_code(self,value):
        """
        Inputs
            value   Integer

        See the description of attribute success_code for more information
        """
        self.__success_code = value

    def set_ref_success_code(self,value):
        """
        Inputs
            value   Integer
        See the description of attribute success_code for more information
        """
        self.__ref_success_code = value

    def set_converging_val(self,value):
        """
        Inputs
            value   Float
        Highest value for which the simulation has converged up to the moment
        this method is called
        """
        self.__converging_val = value

###############################################################################
#                                 RESETTERS                                   #
###############################################################################
    def reset_val(self):
        """
        Reset value of attribute val to its reference value: 0.
        """
        self.__val = 0.

###############################################################################
#                               MAIN METHODS                                  #
###############################################################################

    def increase_nit(self):
        """
        Increase value of attribute nit.
        This method must be called when a simulation is run.
        """
        self.__nit += 1

    def get_path_store_res_dir(self):
        """
        Return the path in which the results are saved.
        """
        return path.abspath(path.join(self.main_dir,self.store_res_dir))

    def create_working_directory(self):
        """
        A directory in which all the simulations will be made is created.
        The files that are in self.simu_material_dir are copie into this new directory.
        If self.store_res_dir does not exist in main_dir, a directory named self.store_res_dir is created
        """
        if path.exists(path.join(self.main_dir,self.simu_dir)):
            rmtree(path.join(self.main_dir,self.simu_dir), ignore_errors=True)   #added 19_07_2018
        copytree(path.abspath(path.join(self.main_dir,self.simu_material_dir)),path.join(self.main_dir,self.simu_dir))

        if path.exists(path.join(self.main_dir,self.store_res_dir)):
            rmtree(path.join(self.main_dir,self.store_res_dir), ignore_errors=True)  #added 19_07_2018
        mkdir(path.join(self.main_dir,self.store_res_dir))

    def reset_res(self):
        """
        Reset value of attribute res to {} (=a dictionary without any keys)
        """
        self.__res = {}

    def set_res(self):
        """
        Set the value of attribute res.
        This method has te be called when a simulation has converged and before
        the result is written into a file by method write_res
        """
        self.reset_res()

        for var in self.list_inputs:
            if var in self.dict_var_to_fix:
                self.__res[var] = self.dict_inputs[var]
            else:
                #After a simulation, self.dict_inputs is not modified (it would
                #be a nonsense to change self.dict_inputs if no simulation has
                #to be done), but self.around_simulation.dict_iter_var is modified,
                #that is the reason why it is necessary to extract the values
                #in self.around_simulation.dict_iter_var.
                self.__res[var] = self.around_simulation.dict_iter_var[var]


    def set_dict_inputs(self,ref=False):
        """
        Set the value of attribute dict_inputs
        The values of the iterations variables comes from the last simulation
        which has converged. The values of the parameters that have to be
        fixed are calculated with the functions of self.dict_var_to_fix.

        If ref=True, val is given the value 0 and the iteration variables are
        given the values they have in self.simulation0.dict_iter_var.
        """
        if ref:
            self.reset_val()
            self.__dict_inputs = copy(self.around_simulation0.dict_iter_var)

        else:
            #Get the iteration variables and their values
            self.__dict_inputs = copy(self.around_simulation.dict_iter_var)

        #Get the values of the variables that have to be fixed
        for var_to_fix in self.dict_var_to_fix:
            self.dict_inputs[var_to_fix] = self.dict_var_to_fix[var_to_fix](self.val)

        #Set the value of attribute list_inputs if it has no value
        if self.list_inputs == []:
            self.__list_inputs = list(self.dict_inputs.keys())
            self.list_inputs.sort()

    def write_res(self,ref=False):
        """
        Write in self.var_to_follow_path the values of the inputs at the end
        of the simulation
        """
        with open(self.var_to_follow_path,'a') as output:
            if ref:
                output.write('val'.ljust(50)+';')
                for var in self.list_inputs[:-1]:
                    output.write(var.ljust(50)+';')
                output.write(self.list_inputs[-1]+'\n')

            output.write(str(self.val).ljust(50)+';')
            for var in self.list_inputs[:-1]:
                output.write(str(self.res[var]).ljust(50)+';')
            output.write(str(self.res[var])+'\n')

    def clean_var_to_follow(self):
        """
        If the file self.var_to_follow_path exists, it is erased when this
        method is called
        """
        if path.exists(self.var_to_follow_path):
            remove(self.var_to_follow_path)

    def fauto_simu(self,ref=False,final_cleaning=False):
        """
        Erase the old simulation files from the simulation directory and run a
        simulation with the current values of the iteration variables
        """
        #Create an object of type Automatic_Simulation, which will make it easy
        #to run the simulation
        #Check inputs only for the target case
        logging.debug('Val %s' % self.val)
        if (not ref) and (self.val == 1.) :
            tmp_check = self.check_inputs
            logging.debug('Performing input check on the target case (run %s)' % self.nit)
        else :
            tmp_check = []

        logging.debug('Input of the current case:')
        for key in self.dict_inputs.keys():
            logging.debug('%s = %s' % (key,self.dict_inputs[key]))

        auto_simu = Automatic_Simulation(simu_dir=path.join(self.main_dir,self.simu_dir),
                              dict_inputs=self.dict_inputs,
                              dymosim_path = self.__dymosim_path,
                              logfile=True,
                              timeout=self.timeout,
                              copy_dsres_to=path.join(self.get_path_store_res_dir(),str(self.val)+'.mat'),
                              check_inputs=tmp_check,
                              linux = self.linux,
                              without_modelicares = True) # A garder à False car sinon write_in_dsin efface dic_inputs... update 12/2022: writ_in_dsin modifié pour ne pas vider dict_inputs

        #Write in log file
        logging.info('Time = '+get_cur_time()+' \t'+'Current value: '+str(self.val))

        self.set_success_code(99)
        self.increase_nit()

        #Run the simulation
        auto_simu.single_simulation()


        #If the simulation has converged
        if auto_simu.success_code == 0:

            #If an initialization script has to be created
            if self.gen_scripts_ini:
                #If the simulation state is the reference state
                if ref:
                    self.around_simulation0.generated_script_options={'file_name':path.join(self.get_path_store_res_dir(),str(self.val)+'.mos')}
                    self.around_simulation0.create_script_ini()
                else:
                    # -----> Option should be added to the dictionary and not reset !!!!!
                    self.around_simulation.generated_script_options={'file_name':path.join(self.get_path_store_res_dir(),str(self.val)+'.mos')}
                    self.around_simulation.create_script_ini()

            if ref:
                logging.info('Time = '+get_cur_time()+' \t'+'Reference simulation has converged')
                self.set_ref_success_code(0)
                self.__around_simulation = copy(self.around_simulation0)
            else:
                logging.info('Time = '+get_cur_time()+' \t'+'Simulation has converged')

            #If this simulation is the first to converge, the next values of the iteration variables will be built from the mat result file.
            if self.converging_val == None:
                self.around_simulation.iter_var_values_options['source'] = 'from_mat'


            self.set_success_code(0)
            self.set_converging_val(self.val)
            self.around_simulation.mat = path.join(self.get_path_store_res_dir(),str(self.val)+".mat")
            self.around_simulation.set_dict_iter_var()
            self.set_res()
            self.write_res(ref=ref)

        else:
            self.set_success_code(auto_simu.success_code)

            if ref:
                self.set_ref_success_code(auto_simu.success_code)
                logging.info('Time = '+get_cur_time()+' \t'+'Reference simulation has not converged. Success_code = '+str(self.ref_success_code))
            else:
                logging.info('Time = '+get_cur_time()+' \t'+'Simulation has not converged. Success_code = '+str(self.success_code))
        if final_cleaning:
            auto_simu.cleaning()

    def check_ref_simulation(self):
        """
        Run the simulation in the reference state
        """
        #Erase the file in which the values of the inputs at the end of the
        #simulations are saved
        self.clean_var_to_follow()

        #reset the values of the inputs
        self.set_dict_inputs(ref=True)

        #Run the simulation
        self.fauto_simu(ref=True)

    def change_val(self):
        """
        Adapt the step if it is necessary and change the value of attribute val.
        The step is divided by 2 when a simulation does not converge.
        """
        if self.success_code == 1:
            self.__cur_step = float(self.cur_step)/2.
        elif self.success_code in [2,3]:
            logging.info('Time = '+get_cur_time()+' \t'+'Method change_val has been called whereas the success_code is in [2,3] which \
            is not normal. The methods designed in this script can only help to initialize the simulations. If the simulation fails \
            whereas the initialization has been a success, it is not useful to decrease the step')
            self.__cur_step = 0
        else:
            if self.val+self.cur_step > 1:
                self.__cur_step = 1.-self.val
        if self.converging_val == None:
            self.__val = self.cur_step
        else:
            self.__val = self.converging_val + self.cur_step

    def working_point_modification(self,final_cleaning=False,skip_reference_simulation=False):
        """
        Main method of this class.
        It tries to reach the target state from the reference state.
            The step is adapted with change_val depending on the success of the simulations
            Before a simulation is run, the variables are initialized to
                Their calculated value if it is a variable whose value should be imposed
                The value calculated by Dymola in the last simulation that has converged if it is an iteration variable
        """
        if skip_reference_simulation:
            self.skip_reference_simulation()

        if self.ref_success_code == 0 or skip_reference_simulation:
            while self.nit < self.nit_max and (self.converging_val == None or self.converging_val < 1) and self.success_code not in [2,3] :
                self.change_val()
                if self.crit_check() :
                    break
                if self.cur_step < self.min_step_val : #Check after change_val call
                    break
                self.set_dict_inputs(ref=False)
                logging.debug(".nit : %s\n.converging_val : %s\n.around_simulation.mat : %s\n.around_simulation._source_ : %s" %(self.nit,self.converging_val,self.around_simulation.mat,self.around_simulation.iter_var_values_options['source']))
                self.fauto_simu(ref=False,final_cleaning=final_cleaning)

            if not(self.nit < self.nit_max):
                logging.info('Time = '+get_cur_time()+' \t'+'STOP: maximum number of iterations reached.')
            if self.converging_val != None and not(self.converging_val < 1):
                logging.info('Time = '+get_cur_time()+' \t'+'FINISHED: Target values reached.')
            if self.success_code in [2,3]:
                logging.info('Time = '+get_cur_time()+' \t'+'STOP: Simulation initialization has succeeded, but simulation has failed or was not given enough time to converge')

    def crit_check(self):
        """
        Check whether the step-size and the max-number-of-iterations criteria has been met
        """
        check = False
        if self.success_code == 1 : #Check criteria only if the previous iteration did not initialize
            if (self.cur_step < self.min_step_val) : #Minimum step size criterium
                logging.info('Time = '+get_cur_time()+' \t'+'STOP: The step ('+str(self.cur_step)+') has crossed the minimum allowed value: '+str(self.min_step_val))
                check = True
            elif ( (self.val + self.cur_step*(self.nit_max - self.nit - 1)) < 1. ) : #Max number of step criterium (with "forecast")
                logging.info('Time = '+get_cur_time()+' \t'+'STOP: Impossible to success before hitting the number of iterations limit: '+str(self.nit_max))
                logging.info('Time = '+get_cur_time()+' \t'+'STOP: Completed iterations: '+str(self.nit)+'; next value: '+str(self.val)+'; current step: '+str(self.cur_step))
                check = True
        return check

    def skip_reference_simulation(self):
        logging.info('Time = '+get_cur_time()+' \t'+'Reference simulation is not launched. It is safer to choose skip_reference_simulation=False')
        self.__around_simulation = copy(self.around_simulation0)

###############################################################################
#                            CLASS Dict_Var_To_Fix                            #
###############################################################################

class Dict_Var_To_Fix(object):
    """
    This class makes it easier to create the attribute dict_var_to_fix of the objects
    of class Working_Point_Modification in the case there are only a ref value and
    a target value.
    """
    def __init__(self,option,dict_var_to_fix=None,dict_auto_var_to_fix=None):
        if dict_var_to_fix == None:
            dict_var_to_fix = {}

        self.__option = option
        self.__dict_var_to_fix = dict_var_to_fix
        self.__dict_auto_var_to_fix = dict_auto_var_to_fix

    @property
    def option(self):
        """
        Type: String
        Available values for option are
            'manual'        -> dict_var_to_fix is directly used
            'automatic'     -> dict_var_to_fix is built from dict_auto_var_to_fix
        """
        return self.__option

    @property
    def dict_var_to_fix(self):
        """
        Type: Dictionary
        Dict_var_to_fix is a dictionary which associates
            key     name of the variable whose value must be fixed
            value   Function which returns the value of variable key when val is x
                    0 -> reference value of key
                    1 -> target value of key
        """
        return self.__dict_var_to_fix

    @property
    def dict_auto_var_to_fix(self):
        """
        Type: Dictionary
        This dictionary is used if option == 'automatic'
        It associates
            key     name of the variable whose value must be fixed
            value   (ref_val,target_val) : A 2-tuple composed of the value of
                    the variable key in the reference state and the target value
                    of the variable key
        """
        return self.__dict_auto_var_to_fix

    def set_dict_var_to_fix(self):
        """
        Set the value of attribute dict_var_to_fix when option is 'automatic'.
        If option is 'manual', attribute dict_var_to_fix already has a value.

        Create a function for each variable, which returns
            function(0) -> ref_val
            function(1) -> target_val
        """
        if self.option == 'automatic':
            for var in self.dict_auto_var_to_fix:
                ref_val = self.dict_auto_var_to_fix[var][0]
                target_val = self.dict_auto_var_to_fix[var][1]
                self.__dict_var_to_fix[var] = self.f_creator(ref_val,target_val)

    def f_creator(self,ref_val,target_val):
        """
        Return the linear function returning
            ref_val if it is given 0
            target_val if ti is given 1
        This function is used in method set_dict_var_to_fix of class Dict_Var_To_Fix
        when option == 'automatic'
        """
        def f(x):
            if x<0 or x>1:
                exit("x has to be between 0 and 1")
            else:
                return ref_val+x*(target_val-ref_val)
        return f

if __name__ == '__main__':
    print('\n  AUTODIAGNOSTIC\n  ==============\n')
