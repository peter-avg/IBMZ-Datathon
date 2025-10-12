"""AI extraction service for extracting entities from transcript text."""

import re
from typing import List, Dict, Any
from models.domain import ExtractionResult, ExtractedSymptom, ExtractedMedication


class AIExtractor:
    """AI-powered entity extraction from medical transcript text."""
    
    def __init__(self):
        """Initialize the AI extractor with predefined patterns."""
        # Common medical symptoms patterns
        self.symptom_patterns = [
            r'\b(headache|head pain|migraine)\b',
            r'\b(fever|temperature|hot)\b',
            r'\b(cough|coughing|hacking)\b',
            r'\b(nausea|nauseous|sick to stomach)\b',
            r'\b(fatigue|tired|exhausted|weak)\b',
            r'\b(pain|ache|hurts|sore)\b',
            r'\b(dizziness|dizzy|lightheaded)\b',
            r'\b(shortness of breath|breathing problems|can\'t breathe)\b',
            r'\b(chest pain|chest discomfort)\b',
            r'\b(joint pain|arthritis|stiffness)\b',
            r'\b(diarrhea|loose stools|bowel problems)\b',
            r'\b(constipation|can\'t go|bowel movement)\b',
            r'\b(insomnia|can\'t sleep|sleep problems)\b',
            r'\b(anxiety|worried|nervous)\b',
            r'\b(depression|sad|down)\b'
        ]
        
        # Common medication patterns
        self.medication_patterns = [
            r'\b(aspirin|ibuprofen|acetaminophen|tylenol)\b',
            r'\b(penicillin|amoxicillin|antibiotic)\b',
            r'\b(insulin|metformin|diabetes medication)\b',
            r'\b(lisinopril|blood pressure medication)\b',
            r'\b(atorvastatin|cholesterol medication)\b',
            r'\b(omeprazole|stomach medication)\b',
            r'\b(lorazepam|xanax|anxiety medication)\b',
            r'\b(warfarin|coumadin|blood thinner)\b',
            r'\b(prednisone|steroid)\b',
            r'\b(levothyroxine|thyroid medication)\b'
        ]
        
        # Duration patterns
        self.duration_patterns = [
            r'\b(\d+)\s*(days?|weeks?|months?|years?)\b',
            r'\b(for|since)\s+(\d+)\s*(days?|weeks?|months?|years?)\b',
            r'\b(about|around|approximately)\s+(\d+)\s*(days?|weeks?|months?|years?)\b'
        ]
        
        # Intensity patterns
        self.intensity_patterns = [
            r'\b(mild|slight|minor)\b',
            r'\b(moderate|medium|somewhat)\b',
            r'\b(severe|bad|terrible|awful)\b',
            r'\b(\d+)\s*(out of|/)\s*10\b',
            r'\b(scale|rating)\s*(of|at)\s*(\d+)\b'
        ]
        
        # Frequency patterns
        self.frequency_patterns = [
            r'\b(daily|every day|once a day)\b',
            r'\b(twice daily|2x daily|twice a day)\b',
            r'\b(weekly|once a week)\b',
            r'\b(monthly|once a month)\b',
            r'\b(as needed|when needed|prn)\b',
            r'\b(\d+)\s*(times?)\s*(daily|per day|a day)\b'
        ]
    
    def extract_entities(self, text: str) -> ExtractionResult:
        """
        Extract symptoms and medications from transcript text.
        
        Args:
            text: The transcript text to analyze
            
        Returns:
            ExtractionResult containing extracted entities
        """
        if not text or not text.strip():
            return ExtractionResult(raw_text=text)
        
        text_lower = text.lower()
        
        # Extract symptoms
        symptoms = self._extract_symptoms(text_lower)
        
        # Extract medications
        medications = self._extract_medications(text_lower)
        
        return ExtractionResult(
            symptoms=symptoms,
            medications=medications,
            raw_text=text
        )
    
    def _extract_symptoms(self, text: str) -> List[ExtractedSymptom]:
        """Extract symptoms from text."""
        symptoms = []
        
        for pattern in self.symptom_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                symptom_name = match.group(1).title()
                
                # Extract additional context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Extract duration, intensity, and recurrence
                duration = self._extract_duration(context)
                intensity = self._extract_intensity(context)
                recurrence = self._extract_recurrence(context)
                
                symptom = ExtractedSymptom(
                    name=symptom_name,
                    duration=duration,
                    intensity=intensity,
                    recurrence=recurrence,
                    confidence=0.8  # Mock confidence score
                )
                
                # Avoid duplicates
                if not any(s.name.lower() == symptom_name.lower() for s in symptoms):
                    symptoms.append(symptom)
        
        return symptoms
    
    def _extract_medications(self, text: str) -> List[ExtractedMedication]:
        """Extract medications from text."""
        medications = []
        
        for pattern in self.medication_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                med_name = match.group(1).title()
                
                # Extract additional context around the match
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end]
                
                # Extract strength, frequency, and duration
                strength = self._extract_strength(context)
                frequency = self._extract_frequency(context)
                duration = self._extract_duration(context)
                
                medication = ExtractedMedication(
                    name=med_name,
                    strength=strength,
                    frequency=frequency,
                    duration=duration,
                    confidence=0.8  # Mock confidence score
                )
                
                # Avoid duplicates
                if not any(m.name.lower() == med_name.lower() for m in medications):
                    medications.append(medication)
        
        return medications
    
    def _extract_duration(self, context: str) -> str:
        """Extract duration information from context."""
        for pattern in self.duration_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 2:
                    return f"{match.group(1)} {match.group(2)}"
                elif len(match.groups()) >= 3:
                    return f"{match.group(2)} {match.group(3)}"
        return None
    
    def _extract_intensity(self, context: str) -> str:
        """Extract intensity information from context."""
        for pattern in self.intensity_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 1:
                    return match.group(1)
                elif len(match.groups()) >= 3:
                    return f"{match.group(2)}/10"
        return None
    
    def _extract_recurrence(self, context: str) -> str:
        """Extract recurrence pattern from context."""
        recurrence_keywords = [
            'intermittent', 'occasional', 'sporadic', 'episodic',
            'constant', 'continuous', 'persistent', 'chronic',
            'acute', 'sudden', 'gradual', 'progressive'
        ]
        
        for keyword in recurrence_keywords:
            if keyword in context:
                return keyword.title()
        
        return None
    
    def _extract_strength(self, context: str) -> str:
        """Extract medication strength from context."""
        strength_patterns = [
            r'\b(\d+)\s*(mg|milligrams?)\b',
            r'\b(\d+)\s*(ml|milliliters?)\b',
            r'\b(\d+)\s*(units?)\b',
            r'\b(\d+)\s*(tablets?|capsules?|pills?)\b'
        ]
        
        for pattern in strength_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                return f"{match.group(1)} {match.group(2)}"
        
        return None
    
    def _extract_frequency(self, context: str) -> str:
        """Extract medication frequency from context."""
        for pattern in self.frequency_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                if len(match.groups()) >= 1:
                    return match.group(0)
        return None
    
    def extract_from_transcript_stream(self, transcript_stream: List[Dict[str, Any]]) -> ExtractionResult:
        """
        Extract entities from a stream of transcript entries.
        
        Args:
            transcript_stream: List of transcript entries with 'text' field
            
        Returns:
            Combined extraction result from all transcript entries
        """
        all_text = " ".join([entry.get("text", "") for entry in transcript_stream])
        return self.extract_entities(all_text)


# Global instance
ai_extractor = AIExtractor()
