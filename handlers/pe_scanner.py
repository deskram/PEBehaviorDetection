import os
import pickle
import joblib
import pefile
import tempfile

def extract_infos(fpath):
    res = {}
    pe = pefile.PE(fpath)

    res['Machine'] = pe.FILE_HEADER.Machine
    res['SizeOfOptionalHeader'] = pe.FILE_HEADER.SizeOfOptionalHeader
    res['Characteristics'] = pe.FILE_HEADER.Characteristics
    res['MajorLinkerVersion'] = pe.OPTIONAL_HEADER.MajorLinkerVersion
    res['MinorLinkerVersion'] = pe.OPTIONAL_HEADER.MinorLinkerVersion
    res['SizeOfCode'] = pe.OPTIONAL_HEADER.SizeOfCode
    res['SizeOfInitializedData'] = pe.OPTIONAL_HEADER.SizeOfInitializedData
    res['SizeOfUninitializedData'] = pe.OPTIONAL_HEADER.SizeOfUninitializedData
    res['AddressOfEntryPoint'] = pe.OPTIONAL_HEADER.AddressOfEntryPoint
    res['BaseOfCode'] = pe.OPTIONAL_HEADER.BaseOfCode

    try:
        res['BaseOfData'] = pe.OPTIONAL_HEADER.BaseOfData
    except AttributeError:
        res['BaseOfData'] = 0

    res['ImageBase'] = pe.OPTIONAL_HEADER.ImageBase
    res['SectionAlignment'] = pe.OPTIONAL_HEADER.SectionAlignment
    res['FileAlignment'] = pe.OPTIONAL_HEADER.FileAlignment
    res['MajorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MajorOperatingSystemVersion
    res['MinorOperatingSystemVersion'] = pe.OPTIONAL_HEADER.MinorOperatingSystemVersion
    res['MajorImageVersion'] = pe.OPTIONAL_HEADER.MajorImageVersion
    res['MinorImageVersion'] = pe.OPTIONAL_HEADER.MinorImageVersion
    res['MajorSubsystemVersion'] = pe.OPTIONAL_HEADER.MajorSubsystemVersion
    res['MinorSubsystemVersion'] = pe.OPTIONAL_HEADER.MinorSubsystemVersion
    res['Subsystem'] = pe.OPTIONAL_HEADER.Subsystem
    res['LoaderFlags'] = pe.OPTIONAL_HEADER.LoaderFlags
    res['NumberOfRvaAndSizes'] = pe.OPTIONAL_HEADER.NumberOfRvaAndSizes
    res['SectionsNb'] = len(pe.sections)

    entropy = [section.get_entropy() for section in pe.sections]
    res['SectionsMeanEntropy'] = sum(entropy) / float(len(entropy)) if entropy else 0

    return res

def analyze_pe_file(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as temp_file:
        temp_file.write(file.read())
        temp_file_path = temp_file.name

    try:
        clf = joblib.load('models/classifier.pkl')
        features_list = pickle.load(open('models/features.pkl', 'rb'))

        data = extract_infos(temp_file_path)

        pe_features = [data.get(feature, 0) for feature in features_list]

        EXPECTED_FEATURES_COUNT = len(pe_features)
        if len(pe_features) != EXPECTED_FEATURES_COUNT:
            raise Exception(f"Expected {EXPECTED_FEATURES_COUNT} features, but got {len(pe_features)}")

        result = clf.predict([pe_features])[0]
        classification = 'malicious' if result == 1 else 'legitimate'
        
        return {
            'classification': classification,
            'features': data
        }

    except Exception as e:
        raise Exception(f"Error processing PE file: {str(e)}")
    
    finally:
        try:
            os.remove(temp_file_path)
        except Exception as e:
            print(f"Warning: Unable to delete the temporary file {temp_file_path}")
