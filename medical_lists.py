# medical_terms.py

known_terms = [
    "basophils",
    "eosinophils",
    "haematocrit",
    "haemoglobin",
    "lymphocytes",
    "monocytes",
    "neutrophils",
    "neutrophils ratio",
    "platelets",
    "red blood cells",
    "white blood cells",
    "neutrophils lymphocytes ratio",
    "rbc",
    "wbc",
    "mch",
    "mchc",
    "mcv",
    "rdw",
    "pcv",
    "nlr",
    "alc",
    "aec",
    "bac",
    "mac",
    "nac",
    "tlc",
    "hct",  

    # add more known terms here...
]

abbreviations_dict = {
    "rbc": "red blood cells",
    "wbc": "white blood cells",
    "mch": "mean corpuscular hemoglobin",
    "mchc": "mean corpuscular hemoglobin concentration",
    "mcv": "mean corpuscular volume",
    "rdw": "red cell distribution width",
    "pcv": "packed cell volume",
    # add more abbreviations here...
}

normalization_dict = {
    "red cell count" : "rbc",
    "total wbc count" : "wbc",
    "total wee count" : "wbc",
    "neutrophils ratio": "nlr",
    "neutrophils lymphocytes ratio": "nlr",
    "platelet count": "platelets",
    "rbc count": "rbc",
    "mch mean cell haemoglobin": "mch",
    "mchc mean cell": "mchc",
    "mcv mean cell volume": "mcv",
    "lymphocytes absolute count": "alc",
    "eosinophils absolute count": "aec",
    "basophils absolute count": "bac",
    "monocytes absolute count": "mac",
    "neutrophils absolute count": "nac",
    "pcv/hct cell volume": "pcv",
    "total leucocyte count": "tlc",
    "net": "hct",
    "mev": "mcv",
    "meuc": "mchc",
    "wac": "wbc",
    "neutrophs": "neutrophils",
    # add more terms here...
}