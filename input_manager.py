"""Input Manager per Blog Generator
Gestisce input completi e configurazioni avanzate
"""

import yaml
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class BlogInput:
    """Classe per gestire tutti gli input del blog generator"""
    topic: str
    intent: str = "informativo"  # informativo, commerciale, educativo
    target_website: str = ""
    business_activity: str = ""
    target_audience: str = "pubblico generale"
    tone: str = "professionale"  # professionale, casual, tecnico
    language: str = "it"
    word_count: int = 2000
    include_cta: bool = True
    seo_focus: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Converte l'input in dizionario per i prompt"""
        return asdict(self)

    def validate(self) -> bool:
        """Valida gli input obbligatori"""
        required_fields = ['topic']
        for field in required_fields:
            if not getattr(self, field):
                logger.error(f"Campo obbligatorio mancante: {field}")
                return False
        return True

class InputManager:
    """Gestisce la configurazione e gli input del sistema"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carica la configurazione dal file YAML"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"File di configurazione {self.config_path} non trovato, uso configurazione di default")
            return self._default_config()
        except yaml.YAMLError as e:
            logger.error(f"Errore nel parsing del file di configurazione: {e}")
            return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Configurazione di default"""
        return {
            'models': {
                'research': 'gpt-4o-mini',
                'outline': 'gpt-4o',
                'drafting': 'gpt-4o',
                'optimization': 'gpt-4o',
                'analysis': 'gpt-4o-mini'
            },
            'seo_config': {
                'keyword_density': {'primary': 1.5, 'secondary': 0.8},
                'readability_target': 65,
                'internal_links_min': 3,
                'external_links_min': 5
            },
            'output': {
                'save_intermediate': True,
                'generate_analytics': True,
                'format': 'markdown'
            }
        }
    
    def create_input_from_args(self, args) -> BlogInput:
        """Crea BlogInput dagli argomenti della command line"""
        return BlogInput(
            topic=getattr(args, 'topic', ''),
            intent=getattr(args, 'intent', 'informativo'),
            target_website=getattr(args, 'website', ''),
            business_activity=getattr(args, 'business', ''),
            target_audience=getattr(args, 'audience', 'pubblico generale'),
            tone=getattr(args, 'tone', 'professionale'),
            word_count=getattr(args, 'words', 2000),
            include_cta=getattr(args, 'cta', True),
            seo_focus=getattr(args, 'seo', True)
        )
    
    def create_input_from_file(self, input_file: str) -> BlogInput:
        """Crea BlogInput da file JSON/YAML"""
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                if input_file.endswith('.yaml') or input_file.endswith('.yml'):
                    data = yaml.safe_load(file)
                else:
                    data = json.load(file)
            
            return BlogInput(**data)
        except Exception as e:
            logger.error(f"Errore nel caricamento del file di input: {e}")
            raise
    
    def create_input_interactive(self) -> BlogInput:
        """Crea BlogInput tramite input interattivo"""
        print("\n=== CONFIGURAZIONE BLOG GENERATOR ===\n")
        
        topic = input("Topic dell'articolo: ").strip()
        if not topic:
            raise ValueError("Il topic è obbligatorio")
        
        print("\nIntento dell'articolo:")
        print("1. Informativo")
        print("2. Commerciale") 
        print("3. Educativo")
        intent_choice = input("Scegli (1-3) [1]: ").strip() or "1"
        intent_map = {"1": "informativo", "2": "commerciale", "3": "educativo"}
        intent = intent_map.get(intent_choice, "informativo")
        
        target_website = input("Sito web di destinazione (opzionale): ").strip()
        business_activity = input("Attività/servizio da sponsorizzare (opzionale): ").strip()
        target_audience = input("Pubblico target [pubblico generale]: ").strip() or "pubblico generale"
        
        print("\nTono di voce:")
        print("1. Professionale")
        print("2. Casual")
        print("3. Tecnico")
        tone_choice = input("Scegli (1-3) [1]: ").strip() or "1"
        tone_map = {"1": "professionale", "2": "casual", "3": "tecnico"}
        tone = tone_map.get(tone_choice, "professionale")
        
        word_count = input("Numero di parole target [2000]: ").strip()
        try:
            word_count = int(word_count) if word_count else 2000
        except ValueError:
            word_count = 2000
        
        include_cta = input("Includere call-to-action? (s/n) [s]: ").strip().lower()
        include_cta = include_cta != 'n'
        
        return BlogInput(
            topic=topic,
            intent=intent,
            target_website=target_website,
            business_activity=business_activity,
            target_audience=target_audience,
            tone=tone,
            word_count=word_count,
            include_cta=include_cta
        )
    
    def get_model_config(self, agent_type: str) -> str:
        """Ottiene la configurazione del modello per un agente specifico"""
        return self.config.get('models', {}).get(agent_type, 'gpt-4o')
    
    def get_seo_config(self) -> Dict[str, Any]:
        """Ottiene la configurazione SEO"""
        return self.config.get('seo_config', {})
    
    def get_output_config(self) -> Dict[str, Any]:
        """Ottiene la configurazione di output"""
        return self.config.get('output', {})
    
    def save_input_template(self, filename: str = "input_template.yaml") -> None:
        """Salva un template di input per riferimento"""
        template = BlogInput(
            topic="Inserisci il topic qui",
            intent="informativo",  # informativo, commerciale, educativo
            target_website="https://tuosito.it",
            business_activity="Descrivi la tua attività",
            target_audience="Descrivi il pubblico target",
            tone="professionale",  # professionale, casual, tecnico
            word_count=2000
        )
        
        with open(filename, 'w', encoding='utf-8') as file:
            yaml.dump(asdict(template), file, default_flow_style=False, allow_unicode=True)
        
        logger.info(f"Template di input salvato in {filename}")
