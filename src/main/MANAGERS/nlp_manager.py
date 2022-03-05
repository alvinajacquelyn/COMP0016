from main.NLP.LDA.ha_lda import HaLda
from main.NLP.LDA.sdg_lda import SdgLda
from main.NLP.LDA.ihe_lda import IheLda

from main.NLP.STRING_MATCH.module_ha_match import ModuleStringMatchHA
from main.NLP.STRING_MATCH.module_match import ModuleStringMatch
from main.NLP.STRING_MATCH.scopus_ha_match import ScopusStringMatch_HA
from main.NLP.STRING_MATCH.scopus_match import ScopusStringMatch_SDG
from main.NLP.STRING_MATCH.scopus_ihe_match import ScopusStringMatch_IHE

from main.NLP.LDA.predict_publication import ScopusPrediction
from main.NLP.SVM.ha_svm import HaSvm
from main.NLP.SVM.ha_svm_dataset import HaSvmDataset
from main.NLP.VALIDATION.validate_ha_svm import ValidateHASvm
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

   def run_LDA_HA(self) -> None:
        """
            Runs LDA model training for Publication IHE classification
        """
        HaLda().run()

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

    def module_string_match_HA(self) -> None:
        """
            Perform HA string matching (keyword occurences) for modules
        """
        ModuleStringMatchHA().run()


    def scopus_string_match_HA(self) -> None:
        """
            Perform HA string matching (keyword occurences) for publications
        """
        ScopusStringMatch_HA().run()
    

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

    def validate_HA_SVM(self) -> None:
        """
           Validate SVM model results for SDG mapping against string matching 
        """
        ValidateHASvm().run()


    def create_SDG_SVM_dataset(self, modules: bool, publications: bool) -> None:
        """
            Creates the dataset needed to run SDG validation on Svm model predictions
        """
        SdgSvmDataset().run(modules, publications)

    def create_HA_SVM_dataset(self, modules: bool, publications: bool) -> None:
        """
            Creates the dataset needed to run SDG validation on Svm model predictions
        """
        HaSvmDataset().run(modules, publications)

    def run_SVM_SDG(self) -> None:
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        SdgSvm().run()

    def run_SVM_HA(self) -> None:
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        HaSvm().run()

    def create_IHE_SVM_dataset(self) -> None:
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        IheSvmDataset().run()

    def run_SVM_IHE(self) -> None:
        """
            Runs SVM model training for Modules & Publications SDG classification
        """
        IheSvm().run()