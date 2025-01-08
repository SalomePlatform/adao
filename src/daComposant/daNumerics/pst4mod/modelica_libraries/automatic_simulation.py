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
import sys
import logging
from os import path,remove,getcwd,chdir,pardir,mkdir
from shutil import copyfile,move
from buildingspy.io.outputfile import Reader

if sys.version_info[0]<3:
    import subprocess32 as subprocess
else:
    import subprocess

from .functions import get_cur_time, tol_equality

#The library to write in dsin.txt is imported directly in method single_simulation
#It can be either modelicares or write_in_dsin

###############################################################################
#                     CLASS Automatic_Simulation                              #
###############################################################################

class DiscardedInput(Exception):
    pass

###############################################################################
#                     CLASS Automatic_Simulation                              #
###############################################################################

class Automatic_Simulation(object):
    """
    Aim: making it easier to run automatic Dymola simulations.

    Notes:
    - Commentaries are written directly in the code
    - Examples are provided with the code to make it easier to use
    - There is a slight difference between the Python2 and Python3 implementation
    of method singleSimulation

    Required libraries that are not in the standard distribution:
    - modelicares
    - subprocess32 (only for Python2)
    - subprocess (only for Python3)

    New features introduced 02/2019:
    - possibility of performing simulations with dsint.txt and dymosim.exe files
    not nessarily in the same folder
    - possibility of creating a results' folder in another folder
    - possibility of using an equivalent file to dsin.txt but with a different name
    - possibility of modifying the results file name
    - the previous use of this module should remain unchanged compared to the previous version
    - Not yet checked for Linux but should work, Python within a Linux environment is not yet implemented.

    Update 06/2019:
    - correction of set_success_code function in order to consider the directory in which the results mat file is created (and not the default one)

    Update 03/2021:
    - better handling of linux simulations (definition dymosim_path)

    Update 09/2022:
    - bug correction in copy_dsres_to and check_inputs
    """

    def __init__(self,simu_dir,dict_inputs,
                 dymosim_path = None, dsin_name = 'dsin.txt', dsres_path = None,
                 logfile=None,timeout=60,copy_dsres_to=None,
                 copy_initial_dsin=None,without_modelicares=False,linux=False,check_inputs=[]):
        self.__simu_dir = path.abspath(simu_dir)
        self.__dsin_name = path.join(path.abspath(simu_dir),dsin_name)
        if dsres_path is None:
            self.__dsres_path = path.join(path.abspath(simu_dir),'dsres.mat')
        elif path.basename(dsres_path)[-4:] =='.mat':
            self.__dsres_path = dsres_path
        else:
            self.__dsres_path = path.join(path.abspath(dsres_path),'dsres.mat')
        self.__logfile = logfile
        self.__timeout = timeout
        self.__copy_dsres_to = copy_dsres_to
        self.__copy_initial_dsin = copy_initial_dsin
        self.__without_modelicares = without_modelicares
        self.__linux = linux

        if dymosim_path is None:
            if self.linux:
                self.__dymosim_path = path.join(path.abspath(simu_dir),'dymosim')
            else:
                self.__dymosim_path = path.join(path.abspath(simu_dir),'dymosim.exe')
        elif path.isdir(dymosim_path):
            if self.linux:
                self.__dymosim_path = path.join(path.abspath(dymosim_path),'dymosim')
            else:
                self.__dymosim_path = path.join(path.abspath(dymosim_path),'dymosim.exe')
        elif path.isfile(dymosim_path):
            self.__dymosim_path = dymosim_path
        else:
            raise ValueError('Model file or directory not found using %s'%str(dymosim_path))

        self.__success_code = 99

        #Potential separation of standard inputs parameters from time varying inputs (dsu.txt)
        if 'Time' in dict_inputs.keys() : #Reserved keyword for time variation
            logging.info("Reserved variable Time found -> dsu.txt creation")
            dsu_keys = []
            for key in dict_inputs :
                #if hasattr(dict_inputs[key],'__iter__') and not isinstance(dict_inputs[key],str) : #Identifying iterables not string
                if isinstance(dict_inputs[key],(list,tuple)) : #Identifying list or tuples
                    dsu_keys.append(key)
            self.dsu_inputs = {key:dict_inputs[key] for key in dsu_keys} #Dictionary restricted to time varying inputs
            for key in dsu_keys : del dict_inputs[key] #Removing the variable from the standard dictionary
        else :
            self.dsu_inputs = None
        self.__dict_inputs = dict_inputs

        if check_inputs is True:
            self.__check_inputs = dict_inputs.keys()
        else:
            self.__check_inputs = check_inputs

###############################################################################
#                                  GETTERS                                    #
###############################################################################
    @property
    def simu_dir(self):
        """
        Path of the directory in which the simulation will be done (directory which
        contains file dsin.txt or equivalent)
        """
        return self.__simu_dir

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
    def dict_inputs(self):
        """
        Dictionary associating to each variable whose value has to be given to
        dsin.txt (inputs + iteration variables if necessary) its value.
        """
        return self.__dict_inputs

    @property
    def logfile(self):
        """
        log file
        """
        return self.__logfile

    @property
    def timeout(self):
        """
        If a simulation has not converged after timeout, the siumlation is stopped.
        """
        return self.__timeout

    @property
    def copy_dsres_to(self):
        """
        Path of the file where dsres.mat should be copied if simulation converges
        """
        return self.__copy_dsres_to

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
    def copy_initial_dsin_to(self):
        """
        Path of the file where dsin.txt should be copied before the first simulation is run.
        """
        return self.__copy_initial_dsin

    @property
    def without_modelicares(self):
        """
        If True, modelicares is not imported.
        Instead, the script named "writer" is imported. A method of class Writer
        is used to write in dsin.txt.
        """
        return self.__without_modelicares

    @property
    def linux(self):
        """
        If the script has to be run on Linux, this attribute should be setted to True.
        On Linux, the exe file is indeed named "dymosim" instead of "dymosim.exe".
        """
        return self.__linux


    def dymosim_path(self):
        """
        Path of the directory that contains the dymosim.exe (or equivalent) file,
        can be different of simu_dir
        """
        return self.__dymosim_path

    def dsin_name(self):
        """
        Name of the dsint.txt (or equivalent) file, must be inclueded in simu_dir
        """
        return self.__dsin_name

    def dsres_path(self):
        """
        Path of the file in which the results mat file will be created
        """
        return self.__dsres_path
###############################################################################
#                                  SETTERS                                    #
###############################################################################
    def set_success_code(self):
        """
        This function sets the values of the following attributes:
            "success":
                True if simulation has converged (a file named success exists (success. on Linux))
                False if simulation has failed (a file named failure exists (failure. on Linux))
                None if simulation has not converged (For instance if the simulation was not given the time to converge)
            "initsuccess":
                True if the simulation succeeded to initialise (a dsres.mat file is found)
                False if the initialization failed (no dsres.mat file is found)
        """
        if path.exists(self.__dsres_path):
            if self.linux:
                if path.exists(path.join(path.dirname(self.__dsres_path),'success.')):
                    self.__success_code = 0
                elif path.exists(path.join(path.dirname(self.__dsres_path),'failure.')):
                    self.__success_code = 2
                else:
                    self.__success_code = 3
            else:
                if path.exists(path.join(path.dirname(self.__dsres_path),'success')):
                    self.__success_code = 0
                elif path.exists(path.join(path.dirname(self.__dsres_path),'failure')):
                    self.__success_code = 2
                else:
                    self.__success_code = 3
        else:
            self.__success_code  = 1 #Suggestion: We should probably also consider timeout happens durng the initialization phase (neither 'dsres.mat' nor 'failure')

###############################################################################
#                                 RESETTERS                                   #
###############################################################################
    def reset_success_code(self):
        """
        Reset value of attribute success
        """
        self.__success_code = 99
###############################################################################
#                               MAIN METHODS                                  #
###############################################################################

    def cleaning(self):
        """
        Remove the files that are automatically created during a simulation
        """
        if path.exists(path.join(self.simu_dir,"success")):
            remove(path.join(self.simu_dir,"success"))
        if path.exists(path.join(self.simu_dir,"failure")):
            remove(path.join(self.simu_dir,"failure"))
        if path.exists(path.join(self.simu_dir,"null")):
            remove(path.join(self.simu_dir,"null"))
        if path.exists(path.join(self.simu_dir,"dsfinal.txt")):
            remove(path.join(self.simu_dir,"dsfinal.txt"))
        if path.exists(path.join(self.simu_dir,"status")):
            remove(path.join(self.simu_dir,"status"))
        if path.exists(path.join(self.simu_dir,"dslog.txt")):
            remove(path.join(self.simu_dir,"dslog.txt"))
        if path.exists(self.__dsres_path):
            remove(self.__dsres_path)

    def single_simulation(self):
        """
        Run an simulation using dymosim.exe after inserting the values that are
        contained in self.dict_inputs in dsin.txt
        """
        #Import a library to write in dsin.txt
        if self.without_modelicares == True:
            from .write_in_dsin import Write_in_dsin
        else:
            import modelicares

        #Save the value of the current working directory in CUR_DIR
        CUR_DIR = getcwd()

        #It is necessary to change the working directory before running dymosim.exe
        chdir(self.simu_dir)
        if self.logfile:
            logging.info('Time = '+get_cur_time()+' \t'+'Script working in directory '+self.simu_dir)

        #Cleaning the working directory (mandatory to check the intialisation success)
        self.cleaning()

        #File dsin.txt is copied before being changed if it has been given a value
        if self.copy_initial_dsin_to:
            dir_copy_dsin = path.abspath(path.join(self.copy_initial_dsin_to,pardir))
            if not(path.exists(dir_copy_dsin)):
                mkdir(dir_copy_dsin)
            copyfile(src=path.basename(self.__dsin_name),dst=self.copy_initial_dsin_to)

        # Change file dsin.txt
        if self.logfile:
            #print('Changing dsin.txt')
            logging.info('Time = '+get_cur_time()+' \t'+'Changing dsin.txt')
        if self.without_modelicares:
            writer = Write_in_dsin(dict_inputs = self.dict_inputs,filedir = self.simu_dir, dsin_name = path.basename(self.__dsin_name), new_file_name = path.basename(self.__dsin_name))
            writer.write_in_dsin()
        else:
            modelicares.exps.write_params(self.dict_inputs,path.basename(self.__dsin_name))

        #A folder for results file is created if it does not exist (usually for dsres.mat)
        if self.dsres_path:
            dir_dsres_path = path.abspath(path.join(self.__dsres_path,pardir))
            if not(path.exists(dir_dsres_path)):
                mkdir(dir_dsres_path)

        # Simulation launching : execution of dymosim.exe
        if self.logfile:
            #print('Launching simulation')
            logging.info('Time = '+get_cur_time()+' \t'+"Launching simulation")
###############################################################################
#      WARNING: DIFFERENT SOLUTIONS FOR PYTHON 2 AND PYTHON 3                 #
###############################################################################
#Python2 solution - working solution
        if sys.version_info[0]<3:
            try:
                if self.linux:
                    #print('Running dymosim')
                    subprocess.call(str(self.__dymosim_path + ' ' + self.__dsin_name + ' ' + self.__dsres_path),timeout=self.timeout)		#NOT TESTED
                else:
                    #print('Running dymosim.exe')
                    subprocess.call(str(self.__dymosim_path + ' ' + self.__dsin_name + ' ' + self.__dsres_path),timeout=self.timeout)       #NOT TESTED

            except subprocess.TimeoutExpired:
                if self.logfile:
                    logging.info('Time = '+get_cur_time()+' \t'+'Time limit reached. Simulation is stopped.')
                    #Add information about the simulation time when the simulation is stopped
                    try:
                        with open('status','r') as lines:
                            for line in lines:
                                words = line.split()
                                if len(words) > 0:
                                    stop_time = line.split()[-1]
                        logging.info('Simulation time when simulation is stopped: '+str(stop_time))
                    except:
                        pass

#Python3 solution - best solution. Cannot be easily implemented on Python2 because
#the TimeoutExpired exception creates an error (apparently because of subprocess32)
        else:
            try:
                #print('Running dymosim.exe')
                proc = subprocess.Popen([str(arg) for arg in [self.__dymosim_path,self.__dsin_name,self.__dsres_path]],
                                        stderr=subprocess.STDOUT,stdout=subprocess.PIPE,universal_newlines=True)
                dymout, _ = proc.communicate(timeout=self.timeout)
                if self.logfile:
                    logging.debug(dymout)

            except subprocess.TimeoutExpired:
                proc.kill()
                dymout, _ = proc.communicate() #Finalize communication (python guidelines)
                if self.logfile:
                    logging.debug(dymout)
                    logging.info('Time = '+get_cur_time()+' \t'+'Time limit reached. Simulation is stopped.')
                    try:
                        with open('status','r') as lines:
                            for line in lines:
                                words = line.split()
                                if len(words) > 0:
                                    stop_time = line.split()[-1]
                        logging.info('Simulation time when simulation is stopped: '+str(stop_time))
                    except:
                        pass
###############################################################################
#                       END OF WARNING                                        #
###############################################################################

        #Set the value of attribute success
        self.set_success_code()

        #Copy dsres.mat if attribute copy_dsres_to is not None
        if self.success_code == 0:
            logging.info('Time = '+get_cur_time()+' \t'+'Simulation has converged')
            if self.copy_dsres_to:
                move(self.__dsres_path,self.copy_dsres_to) #Test

        elif self.success_code == 1:
            logging.info('Time = '+get_cur_time()+' \t'+'Simulation has failed - Error during initialization')

        elif self.success_code == 2:
            logging.info('Time = '+get_cur_time()+' \t'+'Simulation has failed - Error after the initialization')

        elif self.success_code == 3:
            #The message is written in the TimeoutExpired Exception
            pass
        # Check whether the inputs have been taken into account
        if self.success_code != 1 :
            for key in self.check_inputs :
                if self.copy_dsres_to:
                    outfile = Reader(self.copy_dsres_to,'dymola')
                else:
                    outfile = Reader(self.__dsres_path,'dymola')
                used_val = outfile.values(key)[1][0]
                if self.logfile:
                    logging.debug('Checking %s : %s (set) vs. %s (used)' % (key,self.dict_inputs[key],used_val))
                if not tol_equality((self.dict_inputs[key],outfile.values(key)[1][0])):
                    raise DiscardedInput('Parameter %s: %s set but %s used' % (key,self.dict_inputs[key],used_val))

        #Go back to CUR_DIR
        chdir(CUR_DIR)

if __name__ == '__main__':
    print('\n  AUTODIAGNOSTIC\n  ==============\n')
