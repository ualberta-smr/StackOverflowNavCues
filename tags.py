import pdb
import xml.etree.ElementTree as etree
from pyquery import PyQuery

TAGS_LIST = dict()

def load_tags():
    for event, elem in etree.iterparse('Tags.xml', events=('start', 'end')):
        if event == "start":
            if elem.tag == "row":
                TAGS_LIST[elem.attrib["TagName"].lower()] = elem.attrib["Count"]


QUALITY_WORDS = {
"integrity", "security", "interoperability", "testability", "maintainability",  "traceability",  "accuracy",  "modifiability",  "understandability", "availability", "modularity", "usability", "correctness", "performance",  "verifiability",  "efficiency", "portability", "flexibility,reliability", "testability", "changeability", "analyzability", "stability", "maintain", "maintainable", "modularity", "modifiability", "understandability", "interdependent", "dependency", "encapsulation", "decentralized", "modular", "security", "compliance", "accuracy", "interoperability", "suitability", "functional", "practicality", "functionality", "compliant", "exploit", "certificatesecured", "buffer", "overflow", "policy", "malicious", "trustworthy", "vulnerable", "vulnerability", "accurate", "secure", "vulnerability", "correctness", "accuracy", "conformance", "adaptability", "replaceability", "installability", "portable", "movableness", "movability", "portability", "specification", "migration", "standardized", "l10n", "localization", "i18n", "internationalization", "documentation", "interoperability", "transferability", "resource", "behaviour", "time", "behaviour", "efficient", "efficiency", "performance", "profiled", "optimize", "sluggish", "factor", "penalty", "slower", "fasterslow", "fast", "optimization", "operability", "understandability", "learnability", "useable", "usable", "serviceable", "usefulness", "utility", "useableness", "usableness", "serviceableness", "serviceability", "usability", "gui", "accessibility", "menu", "configure", "convention", "standard", "feature", "focus", "ui", "mouse", "icons", "ugly", "dialog", "guidelines", "click", "default", "human", "convention", "friendly", "user", "screen", "interface", "flexibility", "fault", "tolerance", "recoverability", "maturity", "reliable", "dependable", "responsibleness", "responsibility", "reliableness", "reliability", "dependableness", "dependability", "resilience", "integrity", "stability", "stable", "crashbug", "fails", "redundancy", "error", "failure"
}

MODAL_VERBS = {
    "shall", 
    "should",
    "will",
    "must", 
    "would", 
    "can", 
    "might",
    "could",
    "may",
}

NOUN_IDENTIFIERS = {'NN', 'NNS', 'NNP', 'NNPS'}