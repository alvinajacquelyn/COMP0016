from main.NLP.LDA.sdg_lda import SdgLda
from main.NLP.LDA.ihe_lda import IheLda

from main.NLP.STRING_MATCH.module_match import ModuleStringMatch
from main.NLP.STRING_MATCH.scopus_match import ScopusStringMatch_SDG
from main.NLP.STRING_MATCH.scopus_ihe_match import ScopusStringMatch_IHE

from main.NLP.LDA.predict_publication import ScopusPrediction
from main.NLP.SVM.ha_svm import HaSvm
from main.NLP.SVM.ha_svm_dataset import HaSvmDataset
from main.NLP.SVM.ha_svm_module import HaModuleSvm
from main.NLP.SVM.ha_svm_module_dataset import HASvmModuleDataset
from main.NLP.SVM.ihe_svm_module_dataset import IHESvmModuleDataset
from main.NLP.SVM.ihe_svm_module import IheModuleSvm
from main.NLP.SVM.sdg_svm_pub import SdgPubSvm
from main.NLP.SVM.sdg_svm_pub_dataset import SdgSvmPubDataset
from main.NLP.VALIDATION.validate_sdg_svm import ValidateSdgSvm

from main.NLP.SVM.sdg_svm_dataset import SdgSvmDataset
from main.NLP.SVM.ihe_svm_dataset import IheSvmDataset
from main.NLP.SVM.sdg_svm import SdgSvm
from main.NLP.SVM.ihe_svm import IheSvm

class NLP_SECTION():

    def run_LDA_SDG(self) -> None:
        """
            Runs LDA model training for Module SDG classification
        """
        SdgLda().run()

    def run_LDA_IHE(self) -> None:
        """
            Runs LDA model training for Publication IHE classification
        """
        IheLda().run()


    def module_string_match(self) -> None:
        """
            Perform SDG string matching (keyword occurences) for modules
        """
        ModuleStringMatch().run()
    
    def scopus_string_match_SDG(self) -> None:
        """
            Perform SDG string matching (keyword occurences) for publications
        """
        ScopusStringMatch_SDG().run()

    def scopus_string_match_IHE(self) -> None:
        """
            Perform IHE string matching (keyword occurences) for publications
        """
        ScopusStringMatch_IHE().run()

    def predictScopus(self) -> None:
        """
            Use trained LDA model to perform SDG assignments for Scopus publications
        """
        ScopusPrediction().predict()

    def validate_SDG_SVM(self) -> None:
        """
           Validate SVM model results for SDG mapping against string matching 
        """
        ValidateSdgSvm().run()

    def create_SDG_SVM_dataset(self, modules: bool, publications: bool) -> None: #should we put all the modules training together so they run together?
        """
            Creates the dataset needed to run SDG validation on Svm model predictions
        """
        SdgSvmDataset().run(modules, publications)
        HASvmModuleDataset().run(modules,publications)
        IHESvmModuleDataset.run(modules, publications)

    def run_SVM_SDG(self) -> None: #should we put all the modules training together so they run together?
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        SdgSvm().run()
        HaModuleSvm().run()
        IheModuleSvm().run()

    def create_IHE_SVM_dataset(self) -> None: #should we put all the publications training together so they run together?
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        IheSvmDataset().run()
        SdgSvmPubDataset().run()
        HaSvmDataset().run()
    
    

    def run_SVM_IHE(self) -> None: #should we put all the publications training together so they run together?
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        IheSvm().run()
        SdgPubSvm().run()
        HaSvm.run()



