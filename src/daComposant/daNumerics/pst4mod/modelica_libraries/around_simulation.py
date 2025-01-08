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
import re
from buildingspy.io.outputfile import Reader # To read dsres.mat
from os import path,getcwd,pardir,mkdir
from numpy import mean
from sys import exit
import pandas as pd
import numpy as np
import os

from .functions import get_cur_time, Edit_File

class NotImplementedError(Exception) :
    """
    This exception is raised when there is only one alive (not enough to continue)
    """
    pass


###############################################################################
#                        CLASS Simulation_Files                               #
###############################################################################

class Around_Simulation(object):
    """
    Aim: creating an efficient and user-friendly software dedicated to creating
    initialization scripts for Modelica based simulation tools.

    Notes:
    - Commentaries are written directly in the code
    - Examples are provided with the code to make it easier to use
    - It is recommended to create the build the list of the iteration variables from
    the information that is displayed in the log printed by Dymola during the
    translation (ie: choose source_list_iter_var = 'from_dymtranslog' when it is possible)
    - The derivative of the variables are never considered as iteration variables
    - It should be possible to create the list of the iteration variables from file
    dslog.txt and this script gives an option to do it, but this option has never been
    tested and may also require some modifications.

    Required libraries that are not in the standard distribution:
    - buildingspy
    """

    def __init__(self,dymola_version='Unknown',curdir=getcwd(),source_list_iter_var=None,\
    mo=None,mos=None,copy_from_dym_trans_log=None,dslog_txt=None,mat=None,\
    iter_var_values_options=None,generated_script_options=None,alphabetical_order=True,verbose=True):

        self.verbose = verbose #Boolean, if set to True, some informations are printed to the stdout.

        if iter_var_values_options == None:
            iter_var_values_options={'source':'from_mat','moment':'initial','display':False,'updated_vars':False,'GUI':'Dymola'}

        if generated_script_options == None:
            generated_script_options={'file_name':'Script_ini.mos','dest_dir':None,'pref':'','filters':{},'renamed':None,'compute':{}}

        #Attributes whose values are setted without specific setters
        self.__vdymola = dymola_version
        self.__curdir = path.abspath(curdir)

        #Call setters
        self.source_list_iter_var = source_list_iter_var
        self.mo = mo    #The mo file could be used to check that no fixed value has been added to the list of the iteration variables
        self.mos = mos
        self.copy_from_dym_trans_log = copy_from_dym_trans_log
        self.dslog_txt = dslog_txt
        self.mat = mat
        self.iter_var_values_options = iter_var_values_options
        self.generated_script_options = generated_script_options
        self.__alphabetical_order = alphabetical_order
        #Attributes that cannot be given a value at the creation of the object
        self.__not_found_iter_var = []
        self.__not_found_complex_iter_var = []
        self.__list_iter_var = []
        self.__dict_iter_var = {}
        self.__list_complex_iter_var = []
        self.__dict_complex_iter_var = {}
        self.__dict_iter_var_from_ini = {}  # pour récupérer la valeur du fichier ini.txt
        self.computed_variables = [] #List to store nale of variable computed by user defined function (if any)


###############################################################################
#                                  GETTERS                                    #
###############################################################################

    @property
    def vdymola(self):
        """
        Dymola version
        """
        return self.__vdymola

    @property
    def curdir(self):
        """
        Directory in which the files are contained
        """
        return self.__curdir

    @property
    def source_list_iter_var(self):
        """
        Type of the file in which the iteration variables will be extracted.
        Its values is setted by set_source_list_iter_var
        """
        return self.__source_list_iter_var

    @property
    def mo(self):
        """
        Path of the mo file
        """
        return self.__mo

    @property
    def mos(self):
        """
        Path of the mos file
        """
        return self.__mos

    @property
    def copy_from_dym_trans_log(self):
        """
        Path of the file which contains a copy of the text automatically
        written by Dymola in the translation part of the log window when
        Advanced.LogStartValuesForIteration = true.
        """
        return self.__copy_from_dym_trans_log

    @property
    def dslog_txt(self):
        """
        Path of dslog.txt
        """
        return self.__dslog_txt

    @property
    def mat(self):
        """
        Path of the mat file or list of paths of mat file
        """
        return self.__mat

    @property
    def not_found_iter_var(self):
        """
        List of the iteration variables whose values have been searched and not
        found
        """
        return self.__not_found_iter_var

    @property
    def not_found_complex_iter_var(self):
        """
        List of the images of complex iteration variables whose values has not
        been found
        """
        return self.__not_found_complex_iter_var

    @property
    def list_iter_var(self):
        """
        List of the iteration variables
        """
        return self.__list_iter_var

    @property
    def list_complex_iter_var(self):
        """
        List of iteration variables which are given the value of another variable.
        Classic example: Tp is given the value of T0.
        These values must be identified because the variable that is to be written
        in the initialization script in the case of the example would be T0 and not Tp.
        This list is included in list_iter_var
        """
        return self.__list_complex_iter_var

    @property
    def dict_iter_var(self):
        """
        Dictionary which associates the name of an iteration variable to its value
        """
        return self.__dict_iter_var

    @property
    def dict_iter_var_from_ini(self):  # pour récupérer la valeur du fichier ini.txt
        """
        Dictionary which associates the name of an iteration variable to its value in ini.txt file
        """
        return self.__dict_iter_var_from_ini

    @property
    def dict_complex_iter_var(self):
        """
        Dictionary that is necessary to initialize the values of the iteration
        variables that are in list_complex_iter_var
        Dictionary that associates the value
            key     Variable which should be given a value so that the associated
                    iteration variables are initialized
            value   Dictionary which associates
                key     Associated iteration variable
                value   Value of the associated iteration variables
        Example:
        'Tp1' is initialized with the value 'T0'
        'Tp2' is initialized with the value 'T0'
        dict_complex_iter_var = {'T0':{'Tp1':Tp1_value,'Tp2':Tp2_value}}
        In the initialization script, the mean of Tp1_value and Tp2_value will be written

        This method can only work when the list of the iteration variables has been
        built with the text written in the log during translation (source_list_iter_var = 'from_dymtranslog')
        """
        return self.__dict_complex_iter_var

    @property
    def iter_var_values_options(self):
        """
        Dictionary containing the options that will be used to create the dictionary
        containing the values of the iteration variables
        """
        return self.__iter_var_values_options

    @property
    def generated_script_options(self):
        """
        Dictionary continaing the options that will be used to generate the
        .mos script file
        """
        return self.__generated_script_options

    @property
    def alphabetical_order(self):
        """
        If True, the list of the iteration variables is sorted according to the
        alphabetical order. If False, it is sorted as in the source which is used
        to create the list of the iteration variables.
        """
        return self.__alphabetical_order

###############################################################################
#                                  SETTERS                                    #
###############################################################################
    @source_list_iter_var.setter
    def source_list_iter_var(self,source_list_iter_var):
        """
        Set the value of attribute source_list_iter_var.

        Available values are:
            'from_mos'          The list is created from a .mos file
            The mos file is supposed to be written as follows
                nom_var1 = ...;
                nom_var2 = ...;
            'from_dymtranslog"  The list is created from a .txt file which contains
                                the text automatically written by Dymola in the translation
                                part of the log window when
                                Advanced.LogStartValuesForIteration = true
            'from_dslog'        The list is created from a dslog.txt file
        """
        available_sources = ['from_mos','from_dymtranslog','from_dslog']
        if source_list_iter_var == None:
            print('No value given to self.__source_list_iter_var')
            self.__source_list_iter_var = None
        elif source_list_iter_var in available_sources:
            self.__source_list_iter_var = source_list_iter_var
        else:
            print('The chosen value for source_list_iter_var is not valid. The only valid values are\
            from_mos, from_dymtranslog, from_dslog')

    @mo.setter
    def mo(self,mo_file_name):
        """
        Set the path of the mo file
        """
        if mo_file_name == None:
            self.__mo = None
        else:
            self.__mo = path.join(self.curdir,mo_file_name)

    @mos.setter
    def mos(self,mos_file_name):
        """
        Set the path of the mos file
        """
        if mos_file_name == None:
            self.__mos = None
        else:
            self.__mos = path.join(self.curdir,mos_file_name)

    @copy_from_dym_trans_log.setter
    def copy_from_dym_trans_log(self,copy_from_dym_trans_log):
        """
        Set the path of the file which contains a copy of the text automatically
        written by Dymola in the translation part of the log window when
        Advanced.LogStartValuesForIteration = true.
        """
        if copy_from_dym_trans_log == None:
            self.__copy_from_dym_trans_log = None
        else:
            self.__copy_from_dym_trans_log = path.join(self.curdir,copy_from_dym_trans_log)

    @dslog_txt.setter
    def dslog_txt(self,dslog_txt):
        """
        Set the path of dslog.txt
        """
        if dslog_txt == None:
            self.__dslog_txt = None
        else:
            self.__dslog_txt = path.join(self.curdir,dslog_txt)

    @mat.setter
    def mat(self,mat_file_name):
        """
        Set the path of the mat file
        """
        if not(isinstance(mat_file_name,list)):
            if mat_file_name == None:
                self.__mat = None
            else:
                self.__mat = [path.join(self.curdir,mat_file_name)]
        else:
            self.__mat = []
            for mat_file_name_elem in mat_file_name:
                self.__mat.append(path.join(self.curdir,mat_file_name_elem))


    @iter_var_values_options.setter
    def iter_var_values_options(self,iter_var_values_options):
        """
        Set the value of attribute iter_var_values_options.
        This attribute has to be a dictionary conataining the following keys:
            source (compulsory)
                Available values for source are "from_mat" and "from_mos"
            moment (optional)
                Available values for moment are "initial" and "final"
            display (optional)
                Available values for display are False and True
            updated_vars (optional)
                Available values for updated_vars are False and True
        """
        iter_var_values_options_base = {'source':'from_mat','moment':'initial','display':False,'updated_vars':False,'GUI':'Dymola'}

        for key in list(iter_var_values_options_base.keys()):
            try:
                iter_var_values_options_base[key] = iter_var_values_options[key]
            except:
                if self.verbose :
                    print('Default value used for generated_script_options[\''+str(key)+'\']')

        iter_var_values_options_base['updated_vars'] = iter_var_values_options_base['updated_vars'] and iter_var_values_options_base['display'] #Comparison is only possible if the file is changed on the fly

        try:
            for key in list(iter_var_values_options.keys()):
                if not key in list(iter_var_values_options_base.keys()):
                    print('iter_var_values_options[\''+str(key)+'\'] will not be used: only the following keys are allowed:')
                    for  ki in iter_var_values_options_base.keys() :
                        print(ki)
        except:
            print('iter_var_values_options should be a dictionary')

        self.__iter_var_values_options = iter_var_values_options_base

    @generated_script_options.setter
    def generated_script_options(self,generated_script_options):
        #Default value. It garantees that the structure will always be the same
        generated_script_options_base={'file_name':'Script_ini.mos','dest_dir':None,'pref':'','filters':{},'renamed':None,'compute':{}}

        for key in list(generated_script_options_base.keys()):
            try:
                generated_script_options_base[key] = generated_script_options[key]
            except:
                if self.verbose :
                    print('Default value used for generated_script_options[\''+str(key)+'\']')

        try:
            for key in list(generated_script_options.keys()):
                if not key in list(generated_script_options_base.keys()):
                    print('generated_script_options[\''+str(key)+'\'] will not be used:only values associated to "file_name", "dest_dir", "pref", "filters", "compute" and "renamed" can be taken into account')

        except:
            print('generated_script_options should be a dictionary')

        self.__generated_script_options = generated_script_options_base
###############################################################################
#                                 RESETTERS                                   #
###############################################################################

    def reset_list_iter_var(self):
        """
        Reset the value of attributes list_iter_var and list_complex_iter_var
        """
        self.__list_iter_var = []
        self.__list_complex_iter_var = []

    def reset_not_found_iter_var(self):
        """
        Reset the value of attributes not_found_iter_var and not_found_images_of_complex_iter_var
        """
        self.__not_found_iter_var = []
        self.__not_found_complex_iter_var = []

###############################################################################
#                               MAIN METHODS                                  #
###############################################################################

    def set_list_iter_var(self):
        """
        Set the value of attribute list_iter_var, which contains the list of the iteration variables.
        This list can be created from
            - file dslog.txt (created in case of a translation error) - to be used carefully
            - a .mos file that contains the iteration variables
            - a .txt file that contains the text written by Dymola if option
            Advanced.LogStartValuesForIteration is activated (text written in
            the translation part of the log window)

        This method will look for the iteration variables in a source defined by
        self.source_list_iter_var.
        """
        self.reset_list_iter_var()

        if self.source_list_iter_var == 'from_mos':

            #Regular expression to find the interesting lines - be careful: it does not return the whole line
            input_line_regex = re.compile(r'^[^\\][A-Za-z0-9_.[\]\s]+=\s*-?[0-9]+')

            with open(self.mos,"r") as lines:
                for line in lines:
                    if input_line_regex.search(line):
                        words = [word.strip() for word in line.split('=')]
                        #Add the name of the current iteration variable to the list of iteration variables
                        self.list_iter_var.append(words[0])
                        self.__dict_iter_var_from_ini[words[0]] = words[1]  # valeur du .mos brute_init

        #Only option that can handle the iteration variables that are given the value of other variables
        elif self.source_list_iter_var == 'from_dymtranslog':
            if self.iter_var_values_options['updated_vars'] :
                old_list = self.dymtranslog_read(oldlist=True)
            if self.iter_var_values_options['display'] : #If required, open the 'ini.txt' file to allow modifications (copy)
                #file_display = Popen("Notepad " + self.copy_from_dym_trans_log)
                #file_display.wait()
                Edit_File(self.copy_from_dym_trans_log)
            self.dymtranslog_read()
            if self.iter_var_values_options['updated_vars'] :
                print('Exiting variables: %s' % ' ,'.join(set(old_list).difference(self.list_iter_var)))
                print('Entering variables: %s' % ' ,'.join(set(self.list_iter_var).difference(old_list)))

        elif self.source_list_iter_var == 'from_dslog':
            if self.iter_var_values_options['GUI'] == 'OM' :
                raise NotImplementedError("Automatic reading of the log is still not implemented for OpenModelica") from None
            input_line_regex = re.compile(r'^[^\\][A-Za-z0-9_.[\]\s]+=\s*-?[0-9]+')
            read = False
            with open(self.dslog_txt,'r') as lines:
                for line in lines:
                    if ('Last value of the solution:' in line) or ('Last values of solution vector' in line):
                        read = True
                    elif ('Last value of the solution:' in line) or ('Last values of solution vector' in line):
                        read = False
                    if read and input_line_regex.search(line):
                         words = [word.strip() for word in line.split('=')]
                         #Add the name of the current iteration variable to the list of iteration variables
                         self.list_iter_var.append(words[0])
                         self.__dict_iter_var_from_ini[words[0]] = words[1]  # valeur du dslog.txt brute_init
        else:
            exit('Option given to method set_list_iter_var is not defined. \n\
            Available options are "from_mos", "from_dymtranslog" and "from_dslog".')

        #Alphabetical order
        if self.alphabetical_order:
            self.list_iter_var.sort()

    def dymtranslog_read(self,oldlist=False):
        """
        Method dedicated to the dymtranslog reading
        """
        if oldlist:
            out = []
        else:
            out = self.list_iter_var
        #Regular expression to find the interesting lines
        var_and_start_regex = re.compile(r'[A-Za-z]+[A-Za-z0-9_.[,\s\]]*')
        with open(self.copy_from_dym_trans_log,'r') as lines:
            for line in lines:
                if ('=' in line) and not ('der(' == line[0:4] or 'der (' == line[0:5]) : #Should be a mathematical expression; then, no derivative.
                    unknown_length=False
                    tmp_words = var_and_start_regex.findall(line)
                    words = [word.strip() for word in tmp_words]

                    #Elimination of start
                    try:
                        del words[words.index('start')]
                    except ValueError : #The line does not contain "start" word : this line does not talk about initialization variable -> skip
                        try :
                            del words[words.index('each start')]
                        except ValueError :
                            continue

                    if self.iter_var_values_options['GUI'] == 'OM' :
                        del words[words.index('nominal')] #Added for OpenModelica

                    #If 'E' appears in the right part of a line, it should not be considered as a variable name
                    #because it is almost certainly the 'E' of the scientific writing
                    #Do not call 'E' any of your variable!!
                    if any(s in words[1:] for s in ['E','e']) :
                        words.reverse()
                        try:
                            words.pop(words.index('E'))
                        except ValueError :
                            words.pop(words.index('e')) #Added for OpenModelica
                        words.reverse()

                    #Add the name of the current iteration variable to the list of iteration variables
                    if self.iter_var_values_options['GUI'] == 'OM' :
                        out.append(words[0].split(' ',1)[1]) #OpenModelica : Errors lines copied from the compilation log contains the 'unit' as first word (Integer, Real...)
                    else: #Dymola, default case
                        out.append(words[0])
                        self.__dict_iter_var_from_ini[words[0]] = [word.strip() for word in line.split('=')][1][:-1]  # valeur du ini.txt brute_init


                    #Detection of the iteration variables that are given the values of other variables
                    if not(oldlist) and len(words) >1:
                        self.list_complex_iter_var.append(words[0])
                        self.dict_complex_iter_var[words[1]] = {words[0]:None}
        if oldlist:
            return out

    def set_dict_iter_var(self):
        """
        Set the value of attribute dict_iter_var (and not_found_iter_var).
        dict_iter_var contains the values of the iteration variables that should
        be given to Dymola to help the simulation to initialize.
        These values can be found in a .mat file (containing the result of a simulation)
        or in a .mos file (which has been constructed either manually or automatically).

        This method will use the source specified in self.iter_var_values_options['source']
        to find the values of the iteration variables. It will use the final value of each
        variable if self.iter_var_values_options['source']== 'final' and the initial
        value of each variable if self.iter_var_values_options['source']== 'initial'

        self.iter_var_values_options is a dictionary whose entries must be the following ones:
            'source' (compulsory)
            Possible values:
                - 'from_mat'
                - 'from_mos'

            'moment' (compulsory if the value associated to key 'source' is 'from_mat')
            Possible values:
                - 'initial'
                - 'final'

            'display' (optional)
            Possible values:
                - False
                - True
        """
        #Get special_options
        pref = self.generated_script_options['pref']

        #Reset the list of the iteration variables that have not been found
        self.reset_not_found_iter_var()

        #Create a dictionary to store the intermediate variable values to handle
        #the iteration variables that are given values of other variables
        dict_intermediate_values = {}

        #Get value of filters
        filters = self.generated_script_options['filters']

        if self.iter_var_values_options['source'] == 'from_mat':#It is recommended to use this option

            #Start or final value to be taken from the mat file
            if self.iter_var_values_options['moment'] == 'initial':
                mom = 0
            elif self.iter_var_values_options['moment'] == 'final':
                mom = -1
            else :
                exit("'moment' option can be set only to 'initial' or 'final'")

            # Read file .mat which contains simulation results
            var_to_drop = [] #Because of array expansion
            for mat_file in self.mat:
                structData = Reader(mat_file,'dymola')

                for name_var in self.list_iter_var:
                    varTmp = None #Initialisation
                    res_name_var = name_var

                    if pref != '':
                        if name_var[:len(pref)] == pref:
                            #+1 because of the '.' that is next to pref
                            res_name_var = name_var[len(pref)+1:]

                    # Only if pref is not used (conservative, even if not necessary...)
                    elif not(self.generated_script_options['renamed'] is None):
                        for newname in self.generated_script_options['renamed'].keys() : #For each of renamed component
                            if res_name_var.startswith(newname) : #Check whether the new name in the dictionary matches the current variable
                                res_name_var = self.generated_script_options['renamed'][newname] + res_name_var[len(newname):] #Substitute the new name with the old one (who has to be looked for in the .mat file)

                    for cur_filter in filters:
                    #If the end of the variable name is in list(filters.keys()) -> ex: h_vol,
                    #the corresponding part of the variable is replaced by filers[key] -> ex:h.
                    #The value which will be looked for will therefore be module1.h if the iteration
                    #variable is module1.h_vol. In the script, the name of the iteration variable
                    #(module1.h_vol) will also be given the value calculated for module1.h
                        if cur_filter == name_var[-len(cur_filter):]:
                            res_name_var = res_name_var[:-len(cur_filter)]+filters[cur_filter]

                    try:
                        varTmp = structData.values(res_name_var)[1][mom]
                    except KeyError: #The variable is not found

                        try:
                            node_pos = re.search(r"\[\d+\]",res_name_var).span()  # Position of the node number if any (in case the error is due to a remesh of the model)
                        except AttributeError: #No node number found

                            try:
                                node_pos = re.search(r"\[\]",res_name_var).span()  # Position of empty brakets (all array values are due)
                            except AttributeError :
                                pass
                            else:
                                if res_name_var != name_var :
                                    print('Filters and prefixes still have to be implemented for arrays of unknown size')
                                else :
                                    print(f'{name_var}: unknown size -> Taking all values in .mat (if any)')
                                    tmp = rf'{res_name_var[:node_pos[0]]}\[\d\{res_name_var[node_pos[0]+1:]}'
                                    expanded_vars = structData.varNames(tmp)
                                    for tmp_var in expanded_vars :
                                        self.__dict_iter_var[tmp_var] = structData.values(tmp_var)[1][mom]
                                    if expanded_vars :
                                        var_to_drop.append(name_var)
                                        continue

                        else: #If a node number is found
                            name_start = res_name_var[:node_pos[0]+1]
                            name_end = res_name_var[node_pos[1]-1:]
                            node = int(res_name_var[node_pos[0]+1:node_pos[1]-1]) #Requested node
                            for ii in range(node):
                                try:
                                    varTmp = structData.values(name_start + str(node-ii-1) + name_end)[1][mom] #Look for an upstream node
                                    break
                                except KeyError:
                                    pass

                    if varTmp is None : #If varTmp not defined (name_var not found, not due to remesh)
                        #Try to compute it
                        for var,f in self.generated_script_options['compute'].items() :
                            if res_name_var.endswith(var) :
                                #Collect function inputs
                                root = res_name_var[:-len(var)] #Root path of the variable
                                f_inputs = {}
                                for k,v in f['f_inputs'].items() :
                                    f_inputs[k] = structData.values(root+v)[1][mom]
                                varTmp = f['user_f'](f_inputs)
                                self.computed_variables.append(name_var)

                    if varTmp is None : #If varTmp not defined (name_var not found, not due to remesh, not computed)
                        self.not_found_iter_var.append(name_var)
                    else :

                        #Retrieve the initialization value from the .mat
                        if name_var in self.list_complex_iter_var:
                            dict_intermediate_values[name_var] = varTmp
                        else:
                            self.__dict_iter_var[name_var] = varTmp

                for image_of_complex_var in list(self.dict_complex_iter_var.keys()):
                    for complex_iter_var in list(self.dict_complex_iter_var[image_of_complex_var].keys()):
                        try:
                            self.dict_complex_iter_var[image_of_complex_var][complex_iter_var] = dict_intermediate_values[complex_iter_var]
                        except:#In case the value of variable complex_iter_var has not been found in the mat file
                            if complex_iter_var not in self.not_found_complex_iter_var:
                                self.not_found_complex_iter_var.append(complex_iter_var)
                            else:
                                pass

            for i in var_to_drop :
                self.list_iter_var.remove(i)

        elif self.iter_var_values_options['source'] == 'from_mos':
            #Regular expression to find the interesting lines - be careful: it does not return the whole line
            input_line_regex = re.compile(r'^[^\\][A-Za-z0-9_.[\]\s]+=\s*-?[0-9]+')
            value_regex = re.compile(r'[0-9e+-.]*')

            with open(self.mos,'r') as lines:
                for line in lines:
                    if input_line_regex.search(line):
                        words = [word.strip() for word in line.split("=")]
                        name_var = words[0]
                        if pref+name_var in self.list_iter_var:
                            #The following lines eliminates spaces, ;, and other non-numerical elements
                            value = float(value_regex.findall(words[1])[0])
                            #Add the name of the current iteration variable to the list of iteration variables
                            self.__dict_iter_var[name_var] = value

            #All the iteration variables in self.list_iter_var are added to self.not_found_iter_var if their value has not been found
            for name_var in self.list_iter_var:
                if not name_var in self.dict_iter_var:
                    self.not_found_iter_var.append(name_var)

        else:
            print('Option given to method set_list_iter_var is not defined. \n\
            Available options are "from_mat" and "from_mos".')

        #Sort the not found iteration variables lists
        #Warning: these sorting method puts all the variables whose first letter
        #is uppercase before the variables whose first letter is lowercase.
        self.not_found_iter_var.sort()
        self.not_found_complex_iter_var.sort()


    def create_script_ini(self):
        """
        Create a .mos initialization script.
        The list of the iteration variables must have been created before using this method
        with set_list_iter_var. The values of the iteration variables must have been found
        before using this method with set_dict_iter_var.
        This whole process can be done in one single step with method create_quickly_script_ini.

        self.generated_script_options is a dictionary whose entries must be the following ones:
            file_name   String
                        Name of the .mos file that will be generated
            dest_dir    String
                        path of the directory in which the file should be saved
            pref        String
                        pref + '.' will be added at the beginning of all variables.
                        It is useful if a model has been inserted in a module of a new model
            filters     Dictionary
                        Modifications that have to be applied to the names of the iteration variables
                        Example: {'h_vol':'h'} -> the variable whose name finishes by h_vol will be given the value of the variable whose name finishes by h. Be careful with the use of this filter
        """
        #Put the values of self.generated_script_options in short varaibles to make it easier to write the following function
        file_name,dest_dir = self.generated_script_options['file_name'],self.generated_script_options['dest_dir']
        if dest_dir == None:
            dest_dir=self.curdir

        dest_file_path = path.join(dest_dir,file_name)

        with open(dest_file_path,'w') as output:
            output.write('///////////////////////////////////////////////////////////////////\n')
            output.write('// Script automatically generated by Python ')

            #Date of the creation of the file
            output.write('on '+get_cur_time()+'\n')

            #Dymola version
            output.write('// Dymola version: '+self.vdymola+'\n')

            #Source of the list of iteration variables
            output.write('// List of the iteration variables from file ')
            if self.source_list_iter_var == 'from_mos':
                output.write(self.mos+'\n')
            elif self.source_list_iter_var == 'from_dymtranslog':
                output.write(self.copy_from_dym_trans_log+'\n')
            elif self.source_list_iter_var == 'from_dslog':
                output.write(self.dslog_txt+'\n')

            #Source of the values of the iteration variables
            output.write('// Values of the iteration variables from file ')
            if self.iter_var_values_options['source'] == 'from_mos':
                output.write(self.mos+'\n')
            elif self.iter_var_values_options['source'] == 'from_mat':
                output.write(self.mat[0]+'\n') #The name of the first mat file is kept if several are given
            output.write('///////////////////////////////////////////////////////////////////\n\n\n')

            #Iteration variables whose values have not been found
            if len(self.not_found_iter_var) > 0:
                output.write('///////////////////////////////////////////////////////////////////\n')
                output.write('// Iteration variables whose values have not been found:\n')
                for var_name in self.not_found_iter_var:
                    if var_name not in self.not_found_complex_iter_var:
                        output.write('// '+var_name+'\n')
                output.write('///////////////////////////////////////////////////////////////////\n\n')

            #Iteration variables whose values have not been found
            if len(self.not_found_complex_iter_var) > 0:
                output.write('///////////////////////////////////////////////////////////////////\n')
                output.write('// Complex iteration variables whose values have not been found:\n')
                for var_name in self.not_found_complex_iter_var:
                    output.write('// '+var_name+'\n')

                #Explain the user which values he should give to which variables
                output.write('//It would have no effect to give these complex variables a value in an initialization script.\n')
                output.write('//The initialization should be done by giving the following values to the following variables:\n')
                for complex_iter_var in self.not_found_complex_iter_var:
                    for image_of_complex_iter_var in list(self.dict_complex_iter_var.keys()):
                        if complex_iter_var in list(self.dict_complex_iter_var[image_of_complex_iter_var].keys()):
                            current_iter_vars = list(self.dict_complex_iter_var[image_of_complex_iter_var].keys())
                            output.write('//'+image_of_complex_iter_var+' should be given the mean of the following variables:\n')
                            for cur_var in current_iter_vars:
                                output.write('//- '+cur_var+'\n')
                output.write('///////////////////////////////////////////////////////////////////\n\n')

            #Values of the iteration variables
            output.write('// Iteration variables values:\n')
            #for var_name in self.__list_iter_var:
            #Appending the additional elements to the end of the list
            tmp_not_originally_present = set(self.__list_iter_var) ^ set(self.__dict_iter_var.keys())
            print(f'Variables from expansion: {tmp_not_originally_present}')
            tmp_list = self.__list_iter_var + list(tmp_not_originally_present)
            for var_name in tmp_list :
                if not var_name in self.not_found_iter_var:
                    if not var_name in self.list_complex_iter_var:
                        cmp_str = '' if var_name not in self.computed_variables else '\t//Computed by user defined function'
                        var_value = self.__dict_iter_var[var_name]
                        output.write(var_name.ljust(40)+'\t\t=\t\t'+str(var_value)+';'+cmp_str+'\n')

            #Variables that are given the value of other variables
            if len(list(self.dict_complex_iter_var.keys())) > 0:
                if self.verbose :
                    print("WARNING: Some of the initialising values depends on model's parameters values : automatic changes are unsafe!")
                    print("WARNING: However, some proposals based on previous results are wrote to the script, but commented.")
                    print("WARNING: If required to successfully initialize, the user is invited to check the proposed values and, potentially, uncomment them.")
                output.write('\n// Complex iteration variables values:\n')
                output.write('// WARNING: Some of the following variables may be key parameters of your model.\n')
                output.write('// WARNING: To change their values automatically may be dangerous since it may change the model itself.\n')
                output.write('// WARNING: That is why the following lines are disabled (commented) by default.\n')
                output.write('// WARNING: However, some of them may be initialization parameters (Tstart, ...) and may be safely set.\n')
                output.write('// WARNING: In this case, if you still have initialisation issues, you can safely change their values (uncomment the lines).\n\n')
                for var_name in list(self.dict_complex_iter_var.keys()):
                    #Get the list of values associated to var_name
                    intermediate_list = [self.dict_complex_iter_var[var_name][key] for key in list(self.dict_complex_iter_var[var_name].keys())]
                    #Eliminate values None
                    intermediate_list2 = [elem for elem in intermediate_list if elem != None]
                    #If the list contains at least one value
                    if intermediate_list2 != []:
                        #The mean of the values of the list is calculated
                        var_value = mean([elem for elem in intermediate_list if elem != None])
                        #The mean value is written in the initialization script
                        #Check if any of the values is computed by user function
                        computed = [i for i in intermediate_list if i in self.computed_variables]
                        cmp_str = '' if not computed else '\t//Computed by user defined function'
                        output.write('//'+var_name.ljust(40)+'\t\t=\t\t'+str(var_value)+';'+cmp_str+'\n')

    def create_quickly_script_ini(self):
        """
        Method that:
            - looks for the list of iteration variables with set_list_iter_var;
            - looks for the values of the iteration variables with set_dict_iter_var;
            - crearte a initialization script with create_script_ini.

        """
        self.set_list_iter_var()
        self.set_dict_iter_var()
        self.create_script_ini()

if __name__ == '__main__':
    print('\n  AUTODIAGNOSTIC\n  ==============\n')
