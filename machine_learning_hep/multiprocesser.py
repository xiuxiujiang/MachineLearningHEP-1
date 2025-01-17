#############################################################################
##  © Copyright CERN 2018. All rights not expressly granted are reserved.  ##
##                 Author: Gian.Michele.Innocenti@cern.ch                  ##
## This program is free software: you can redistribute it and/or modify it ##
##  under the terms of the GNU General Public License as published by the  ##
## Free Software Foundation, either version 3 of the License, or (at your  ##
## option) any later version. This program is distributed in the hope that ##
##  it will be useful, but WITHOUT ANY WARRANTY; without even the implied  ##
##     warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    ##
##           See the GNU General Public License for more details.          ##
##    You should have received a copy of the GNU General Public License    ##
##   along with this program. if not, see <https://www.gnu.org/licenses/>. ##
#############################################################################

"""
main script for doing data processing, machine learning and analysis
"""
import os

from machine_learning_hep.processer import Processer
from machine_learning_hep.utilities import merge_method
class MultiProcesser: # pylint: disable=too-many-instance-attributes, too-many-statements
    species = "multiprocesser"
    def __init__(self, datap, run_param, mcordata):
        self.datap = datap
        self.run_param = run_param
        self.mcordata = mcordata
        self.prodnumber = len(datap["multi"][self.mcordata]["unmerged_tree_dir"])
        self.p_period = datap["multi"][self.mcordata]["period"]
        self.p_seedmerge = datap["multi"][self.mcordata]["seedmerge"]
        self.p_fracmerge = datap["multi"][self.mcordata]["fracmerge"]
        self.p_maxfiles = datap["multi"][self.mcordata]["maxfiles"]
        self.p_chunksizeunp = datap["multi"][self.mcordata]["chunksizeunp"]
        self.p_chunksizeskim = datap["multi"][self.mcordata]["chunksizeskim"]
        self.p_nparall = datap["multi"][self.mcordata]["nprocessesparallel"]
        self.lpt_anbinmin = datap["sel_skim_binmin"]
        self.lpt_anbinmax = datap["sel_skim_binmax"]
        self.p_nptbins = len(datap["sel_skim_binmax"])
        #directories
        self.dlper_root = datap["multi"][self.mcordata]["unmerged_tree_dir"]
        self.dlper_pkl = datap["multi"][self.mcordata]["pkl"]
        self.dlper_pklsk = datap["multi"][self.mcordata]["pkl_skimmed"]
        self.dlper_pklml = datap["multi"][self.mcordata]["pkl_skimmed_merge_for_ml"]
        self.d_pklml_mergedallp = datap["multi"][self.mcordata]["pkl_skimmed_merge_for_ml_all"]
        self.d_pklevt_mergedallp = datap["multi"][self.mcordata]["pkl_evtcounter_all"]

        #namefiles pkl
        self.v_var_binning = datap["var_binning"]
        self.n_reco = datap["files_names"]["namefile_reco"]
        self.n_evt = datap["files_names"]["namefile_evt"]
        self.n_evtorig = datap["files_names"]["namefile_evtorig"]
        self.n_gen = datap["files_names"]["namefile_gen"]
        self.lpt_recosk = [self.n_reco.replace(".pkl", "_%s%d_%d.pkl" % \
                          (self.v_var_binning, self.lpt_anbinmin[i], self.lpt_anbinmax[i])) \
                          for i in range(self.p_nptbins)]
        self.lpt_gensk = [self.n_gen.replace(".pkl", "_%s%d_%d.pkl" % \
                          (self.v_var_binning, self.lpt_anbinmin[i], self.lpt_anbinmax[i])) \
                          for i in range(self.p_nptbins)]
        self.lptper_recoml = [[os.path.join(direc, self.lpt_recosk[ipt]) \
                               for direc in self.dlper_pklml] \
                               for ipt in range(self.p_nptbins)]
        self.lper_evtml = [os.path.join(direc, self.n_evt) for direc in self.dlper_pklml]
        self.lper_evtorigml = [os.path.join(direc, self.n_evtorig) for direc in self.dlper_pklml]
        self.lptper_genml = [[os.path.join(direc, self.lpt_gensk[ipt]) \
                              for direc in self.dlper_pklml] \
                              for ipt in range(self.p_nptbins)]
        self.lpt_recoml_mergedallp = [os.path.join(self.d_pklml_mergedallp, self.lpt_recosk[ipt]) \
                                    for ipt in range(self.p_nptbins)]
        self.lpt_genml_mergedallp = [os.path.join(self.d_pklml_mergedallp, self.lpt_gensk[ipt]) \
                                    for ipt in range(self.p_nptbins)]
        self.f_evtml_mergedallp = os.path.join(self.d_pklml_mergedallp, self.n_evt)
        self.f_evtorigml_mergedallp = os.path.join(self.d_pklml_mergedallp, self.n_evtorig)
        self.lper_evt = [os.path.join(direc, self.n_evt) for direc in self.dlper_pkl]
        self.lper_evtorig = [os.path.join(direc, self.n_evtorig) for direc in self.dlper_pkl]

        self.dlper_reco_modapp = datap["analysis"][self.mcordata]["pkl_skimmed_dec"]
        self.dlper_reco_modappmerged = datap["analysis"][self.mcordata]["pkl_skimmed_decmerged"]
        self.d_results = datap["analysis"][self.mcordata]["results"]
        self.lpt_probcutpre = datap["analysis"]["probcutpresel"]
        self.lpt_probcut = datap["analysis"]["probcutoptimal"]
        self.f_evt_mergedallp = os.path.join(self.d_pklevt_mergedallp, self.n_evt)
        self.f_evtorig_mergedallp = os.path.join(self.d_pklevt_mergedallp, self.n_evtorig)

        self.process_listsample = []
        for indexp in range(self.prodnumber):
            myprocess = Processer(self.datap, self.run_param, self.mcordata,
                                  self.p_maxfiles[indexp], self.dlper_root[indexp],
                                  self.dlper_pkl[indexp], self.dlper_pklsk[indexp],
                                  self.dlper_pklml[indexp],
                                  self.p_period[indexp], self.p_chunksizeunp[indexp],
                                  self.p_chunksizeskim[indexp], self.p_nparall,
                                  self.p_fracmerge[indexp], self.p_seedmerge[indexp],
                                  self.dlper_reco_modapp[indexp],
                                  self.dlper_reco_modappmerged[indexp],
                                  self.d_results[indexp])
            self.process_listsample.append(myprocess)


    def multi_unpack_allperiods(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_unpack_par()

    def multi_skim_allperiods(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_skim_par()
        merge_method(self.lper_evt, self.f_evt_mergedallp)
        merge_method(self.lper_evtorig, self.f_evtorig_mergedallp)

    def multi_mergeml_allperiods(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_mergeforml()

    def multi_mergeml_allinone(self):
        for ipt in range(self.p_nptbins):
            merge_method(self.lptper_recoml[ipt], self.lpt_recoml_mergedallp[ipt])
            if self.mcordata == "mc":
                merge_method(self.lptper_genml[ipt], self.lpt_genml_mergedallp[ipt])
        merge_method(self.lper_evtml, self.f_evtml_mergedallp)
        merge_method(self.lper_evtorigml, self.f_evtorigml_mergedallp)

    def multi_apply_allperiods(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_applymodel_par()

    def multi_mergeapply_allperiods(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_mergedec()

    def multi_histomass(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_histomass()

    def multi_efficiency(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_efficiency()

    def multi_scancuts(self):
        for indexp in range(self.prodnumber):
            self.process_listsample[indexp].process_scancuts()
