import PyPDF2
import re
from datetime import datetime
from dateutil import parser

def extract_health_data_from_pdf(pdf_path):
    """
    Extract health-related data from PDF files using text pattern matching
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Initialize data dictionary
        health_data = {
            'raw_text': text.strip(),
            'pregnancy_status': None,
            'gestational_age': None,
            'due_date': None,
            'pregnancy_complications': None,
            'stress_level': None,
            'stress_factors': None,
            'mental_health_notes': None,
            'blood_pressure_systolic': None,
            'blood_pressure_diastolic': None,
            'weight': None,
            'height': None,
            'cholesterol_total': None,
            'cholesterol_ldl': None,
            'cholesterol_hdl': None,
            'blood_sugar': None,
            'heart_rate': None,
            'medications': None,
            'allergies': None,
            'medical_conditions': None,
            'doctor_notes': None,
        }
        
        # Convert text to lowercase for easier pattern matching
        text_lower = text.lower()
        
        # Extract pregnancy-related information
        pregnancy_patterns = [
            r'pregnant|pregnancy|gestational|maternal',
            r'weeks?\s*pregnant',
            r'gestational\s*age:?\s*(\d+)\s*weeks?',
            r'due\s*date:?\s*([0-9/\-]+)',
            r'trimester',
            r'prenatal|antenatal'
        ]
        
        for pattern in pregnancy_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                if not health_data['pregnancy_status']:
                    health_data['pregnancy_status'] = 'Pregnant'
        
        # Extract gestational age
        gestational_match = re.search(r'(?:gestational\s*age|weeks?\s*pregnant):?\s*(\d+)', text_lower)
        if gestational_match:
            health_data['gestational_age'] = f"{gestational_match.group(1)} weeks"
        
        # Extract stress-related information
        stress_patterns = [
            r'stress|anxiety|depression|mental\s*health',
            r'stress\s*level:?\s*(low|moderate|high|severe)',
            r'anxiety\s*level:?\s*(mild|moderate|severe)',
            r'depression|depressed|mood'
        ]
        
        stress_indicators = []
        for pattern in stress_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                stress_indicators.extend(matches)
        
        if stress_indicators:
            health_data['stress_factors'] = ', '.join(set(stress_indicators))
        
        # Extract blood pressure
        bp_pattern = r'blood\s*pressure:?\s*(\d{2,3})[/\-](\d{2,3})'
        bp_match = re.search(bp_pattern, text_lower)
        if bp_match:
            health_data['blood_pressure_systolic'] = int(bp_match.group(1))
            health_data['blood_pressure_diastolic'] = int(bp_match.group(2))
        
        # Extract weight
        weight_patterns = [
            r'weight:?\s*(\d+(?:\.\d+)?)\s*(?:kg|lbs?|pounds?)',
            r'(\d+(?:\.\d+)?)\s*(?:kg|lbs?|pounds?)'
        ]
        
        for pattern in weight_patterns:
            weight_match = re.search(pattern, text_lower)
            if weight_match:
                weight_value = float(weight_match.group(1))
                # Convert lbs to kg if necessary
                if 'lb' in weight_match.group(0) or 'pound' in weight_match.group(0):
                    weight_value = weight_value * 0.453592
                health_data['weight'] = round(weight_value, 2)
                break
        
        # Extract height
        height_patterns = [
            r'height:?\s*(\d+(?:\.\d+)?)\s*(?:cm|m|ft|feet)',
            r'(\d+)\s*(?:cm|m)\s*tall',
            r'(\d+)\s*feet?\s*(\d+)?\s*inch'
        ]
        
        for pattern in height_patterns:
            height_match = re.search(pattern, text_lower)
            if height_match:
                if 'ft' in height_match.group(0) or 'feet' in height_match.group(0):
                    # Convert feet to meters
                    feet = float(height_match.group(1))
                    inches = float(height_match.group(2)) if height_match.group(2) else 0
                    height_value = (feet * 12 + inches) * 0.0254
                else:
                    height_value = float(height_match.group(1))
                    if 'cm' in height_match.group(0):
                        height_value = height_value / 100
                health_data['height'] = round(height_value, 2)
                break
        
        # Extract cholesterol
        cholesterol_patterns = [
            r'cholesterol:?\s*(\d+(?:\.\d+)?)',
            r'total\s*cholesterol:?\s*(\d+(?:\.\d+)?)',
            r'ldl:?\s*(\d+(?:\.\d+)?)',
            r'hdl:?\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in cholesterol_patterns:
            chol_match = re.search(pattern, text_lower)
            if chol_match:
                value = float(chol_match.group(1))
                if 'ldl' in pattern:
                    health_data['cholesterol_ldl'] = value
                elif 'hdl' in pattern:
                    health_data['cholesterol_hdl'] = value
                elif not health_data['cholesterol_total']:
                    health_data['cholesterol_total'] = value
        
        # Extract blood sugar
        blood_sugar_patterns = [
            r'blood\s*sugar:?\s*(\d+(?:\.\d+)?)',
            r'glucose:?\s*(\d+(?:\.\d+)?)',
            r'blood\s*glucose:?\s*(\d+(?:\.\d+)?)'
        ]
        
        for pattern in blood_sugar_patterns:
            sugar_match = re.search(pattern, text_lower)
            if sugar_match:
                health_data['blood_sugar'] = float(sugar_match.group(1))
                break
        
        # Extract heart rate
        hr_pattern = r'heart\s*rate:?\s*(\d+)\s*(?:bpm|beats?)'
        hr_match = re.search(hr_pattern, text_lower)
        if hr_match:
            health_data['heart_rate'] = int(hr_match.group(1))
        
        # Extract medications
        medication_keywords = ['medication', 'medicine', 'drug', 'prescribed', 'taking']
        for keyword in medication_keywords:
            if keyword in text_lower:
                # Extract text around medication mentions
                pattern = rf'{keyword}[:\s]*([^.!?]*)'
                med_matches = re.findall(pattern, text_lower)
                if med_matches:
                    health_data['medications'] = '; '.join(med_matches[:3])  # Limit to first 3 matches
                    break
        
        # Extract allergies
        allergy_keywords = ['allerg', 'allergic to', 'adverse reaction']
        for keyword in allergy_keywords:
            if keyword in text_lower:
                pattern = rf'{keyword}[:\s]*([^.!?]*)'
                allergy_matches = re.findall(pattern, text_lower)
                if allergy_matches:
                    health_data['allergies'] = '; '.join(allergy_matches[:3])
                    break
        
        # Extract medical conditions
        condition_keywords = ['diagnos', 'condition', 'disorder', 'disease', 'syndrome']
        conditions = []
        for keyword in condition_keywords:
            pattern = rf'{keyword}[:\s]*([^.!?]*)'
            condition_matches = re.findall(pattern, text_lower)
            conditions.extend(condition_matches)
        
        if conditions:
            health_data['medical_conditions'] = '; '.join(conditions[:5])
        
        # Clean up extracted data
        for key, value in health_data.items():
            if isinstance(value, str) and value:
                # Clean up text fields
                health_data[key] = value.strip()[:500]  # Limit length to 500 chars
        
        return health_data
        
    except Exception as e:
        raise Exception(f"Error extracting data from PDF: {str(e)}")