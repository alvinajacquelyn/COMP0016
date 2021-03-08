from MANAGERS.module_manager import MODULE_SECTION
from MANAGERS.scopus_manager import SCOPUS_SECTION
from MANAGERS.nlp_manager import NLP_SECTION


def module_manager(initialise, resetDB, scrape, mapToSDG, updateStudentCount):
    module_actions = MODULE_SECTION()
    if initialise:
        module_actions.initialise()
    if resetDB:
        module_actions.resetDB_Table()
    if scrape:
        module_actions.scrapeAllModules()
    if mapToSDG:
        module_actions.map_modules()
    if updateStudentCount:
        module_actions.update_studentsPerModule()

def scopus_manager(renameFiles, scrape, mapToSDG):
    scopus_actions = SCOPUS_SECTION()
    if scrape:
        scopus_actions.scrapeAllPublications()
    if renameFiles:
        scopus_actions.renameGeneratedFiles()
    if mapToSDG:
        scopus_actions.scopusMap()

def nlp_manager(mergeKeywords, initialiseModel, predictScopusData, validateModel):
    nlp_actions = NLP_SECTION()
    if mergeKeywords:
        nlp_actions.merge_SDG_keywords()
    if initialiseModel:
        nlp_actions.initialise_LDA_model()
    if predictScopusData:
        nlp_actions.predictScopus()
    if validateModel:
        nlp_actions.validate()

def main():
    module_manager(initialise=False, resetDB=False, scrape=False, mapToSDG=True, updateStudentCount=False)
    scopus_manager(renameFiles=False, scrape=False, mapToSDG=True)
    nlp_manager(mergeKeywords=False, initialiseModel=False, predictScopusData=False, validateModel=False)

if __name__ == "__main__":
    main()
