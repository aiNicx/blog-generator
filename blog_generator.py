"""Blog Generator Enhanced - Versione migliorata con input completi e step intermedi
Sistema completo per la generazione di articoli SEO ottimizzati in italiano
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from crewai.tools import tool
from typing import Any, Dict, List, Optional
from tavily import TavilyClient
import os
import json
import yaml
import argparse
import logging
from datetime import datetime
from input_manager import InputManager, BlogInput

load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('blog_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlogGeneratorEnhanced:
    """Generatore di blog avanzato con sistema di input completo"""
    
    def __init__(self, config_path: str = "config.yaml", prompts_path: str = "prompts.yaml"):
        self.input_manager = InputManager(config_path)
        self.prompts = self.load_prompts(prompts_path)
        self.tavily_client = self._setup_tavily()
        self.agents = {}
        self.tasks = {}
        
    def load_prompts(self, prompts_path: str) -> Dict[str, str]:
        """Carica i prompt migliorati"""
        try:
            with open(prompts_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.warning(f"File prompt {prompts_path} non trovato, uso prompt di default")
            return self._load_default_prompts()
        except yaml.YAMLError as e:
            logger.error(f"Errore nel parsing dei prompt: {e}")
            return self._load_default_prompts()
    
    def _load_default_prompts(self) -> Dict[str, str]:
        """Carica prompt di default dal file originale"""
        try:
            with open('prompts.yaml', 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except:
            logger.error("Impossibile caricare i prompt")
            raise
    
    def _setup_tavily(self) -> TavilyClient:
        """Configura il client Tavily"""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY non trovata nelle variabili d'ambiente")
        return TavilyClient(api_key=api_key)
    
    def create_llm(self, model_name: str) -> ChatOpenAI:
        """Crea istanza ChatOpenAI con configurazione OpenRouter"""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY non trovata nelle variabili d'ambiente")
        
        # Configura environment per OpenRouter
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
        
        # Rimuovi chiavi Anthropic per evitare conflitti
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]
        
        return ChatOpenAI(
            model=model_name,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Blog Generator Enhanced"
            }
        )
    
    def create_tavily_tool(self):
        """Crea il tool Tavily per gli agenti"""
        @tool
        def tavily_search(query: str) -> str:
            """Ricerca web usando Tavily per risultati e riassunti rilevanti"""
            try:
                results = self.tavily_client.search(query=query, max_results=5)
                return json.dumps(results["results"], indent=2, ensure_ascii=False)
            except Exception as e:
                logger.error(f"Errore nella ricerca Tavily: {e}")
                return json.dumps({"error": f"Ricerca fallita: {str(e)}"}, indent=2)
        return tavily_search
    
    def setup_agents(self, blog_input: BlogInput) -> None:
        """Configura tutti gli agenti con i modelli appropriati"""
        
        # Research Agent - usa modello economico
        self.agents['research'] = Agent(
            role='Ricercatore Esperto',
            goal='Raccogliere informazioni web via Tavily per la generazione di articoli blog',
            backstory='Sei un ricercatore esperto specializzato in ricerche web, estrazione di fatti chiave, statistiche e fonti affidabili per supportare la creazione di contenuti di alta qualità. Ti concentri su informazioni recenti e fattuali per evitare allucinazioni.',
            llm=self.create_llm(self.input_manager.get_model_config('research')),
            tools=[self.create_tavily_tool()],
            verbose=True
        )
        
        # Analysis Agent - nuovo step intermedio con modello economico
        self.agents['analysis'] = Agent(
            role='Analista Strategico',
            goal='Analizzare la ricerca e identificare opportunità strategiche per il contenuto',
            backstory='Sei un analista di contenuti esperto in strategia SEO italiana, specializzato nell\'identificare gap informativi, angoli unici e opportunità di posizionamento per massimizzare l\'efficacia del contenuto.',
            llm=self.create_llm(self.input_manager.get_model_config('analysis')),
            verbose=True
        )
        
        # Outline Agent
        self.agents['outline'] = Agent(
            role='Editor SEO',
            goal='Creare una struttura dettagliata per l\'articolo blog basata sulla ricerca',
            backstory='Sei un editor SEO esperto che progetta strutture di articoli coinvolgenti e ottimizzate per i motori di ricerca con flusso logico, titoli e stime di parole per garantire una copertura completa.',
            llm=self.create_llm(self.input_manager.get_model_config('outline')),
            verbose=True
        )
        
        # Drafting Agent
        self.agents['drafting'] = Agent(
            role='Copywriter Blogger',
            goal='Scrivere una bozza completa dell\'articolo blog basata sulla struttura e ricerca',
            backstory='Sei un blogger esperto che scrive contenuti coinvolgenti e conversazionali che integrano fatti in modo fluido, mantiene le migliori pratiche SEO e garantisce la leggibilità per il pubblico.',
            llm=self.create_llm(self.input_manager.get_model_config('drafting')),
            verbose=True
        )
        
        # Optimization Agent
        self.agents['optimization'] = Agent(
            role='Ottimizzatore SEO e Revisore',
            goal='Ottimizzare la bozza per SEO, lunghezza, coerenza e qualità',
            backstory='Sei un ottimizzatore SEO esperto ed editor che critica e perfeziona i contenuti per massima visibilità sui motori di ricerca, accuratezza fattuale e lucidatura professionale.',
            llm=self.create_llm(self.input_manager.get_model_config('optimization')),
            verbose=True
        )
    
    def setup_tasks(self, blog_input: BlogInput) -> None:
        """Configura tutti i task con i prompt migliorati"""
        input_dict = blog_input.to_dict()
        
        # Research Task
        self.tasks['research'] = Task(
            description=self.prompts["research_description"].format(**input_dict),
            agent=self.agents['research'],
            expected_output="Report JSON strutturato con facts, sources, keywords, opportunities e market_insights"
        )
        
        # Analysis Task - nuovo step intermedio
        self.tasks['analysis'] = Task(
            description=self.prompts["analysis_description"].format(**input_dict),
            agent=self.agents['analysis'],
            context=[self.tasks['research']],
            expected_output="JSON con raccomandazioni strategiche per outline e contenuto"
        )
        
        # Outline Task
        self.tasks['outline'] = Task(
            description=self.prompts["outline_description"].format(**input_dict),
            agent=self.agents['outline'],
            context=[self.tasks['research'], self.tasks['analysis']],
            expected_output="Struttura YAML dettagliata per l'articolo con sezioni, punti elenco e stime parole"
        )
        
        # Drafting Task
        self.tasks['drafting'] = Task(
            description=self.prompts["drafting_description"].format(**input_dict),
            agent=self.agents['drafting'],
            context=[self.tasks['research'], self.tasks['analysis'], self.tasks['outline']],
            expected_output="Bozza Markdown completa dell'articolo con conteggio parole e note SEO"
        )
        
        # Optimization Task
        self.tasks['optimization'] = Task(
            description=self.prompts["optimization_description"].format(**input_dict),
            agent=self.agents['optimization'],
            context=[self.tasks['research'], self.tasks['analysis'], self.tasks['outline'], self.tasks['drafting']],
            expected_output="Articolo Markdown finale ottimizzato e report delle modifiche"
        )
    
    def save_intermediate_results(self, results: Dict[str, Any], blog_input: BlogInput) -> None:
        """Salva risultati intermedi se configurato"""
        if not self.input_manager.get_output_config().get('save_intermediate', False):
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_clean = blog_input.topic.replace(' ', '_').replace('/', '_').lower()
        
        for task_name, result in results.items():
            filename = f"intermediate_{task_name}_{topic_clean}_{timestamp}.json"
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    json.dump(result, file, indent=2, ensure_ascii=False)
                logger.info(f"Risultato intermedio salvato: {filename}")
            except Exception as e:
                logger.error(f"Errore nel salvare risultato intermedio {task_name}: {e}")
    
    def save_final_result(self, result: Any, blog_input: BlogInput) -> str:
        """Salva il risultato finale in un file markdown"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        topic_clean = blog_input.topic.replace(' ', '_').replace('/', '_').lower()
        filename = f"blog_{topic_clean}_{timestamp}.md"
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                if isinstance(result, dict) and 'final_output' in result:
                    file.write(result['final_output'])
                else:
                    file.write(str(result))
            
            logger.info(f"Articolo blog salvato in: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Errore nel salvare il file finale: {e}")
            raise
    
    def generate_analytics_report(self, blog_input: BlogInput, execution_time: float) -> Dict[str, Any]:
        """Genera report analytics dell'esecuzione"""
        if not self.input_manager.get_output_config().get('generate_analytics', False):
            return {}
        
        return {
            'timestamp': datetime.now().isoformat(),
            'input_config': blog_input.to_dict(),
            'execution_time_seconds': execution_time,
            'models_used': {
                agent_type: self.input_manager.get_model_config(agent_type)
                for agent_type in ['research', 'analysis', 'outline', 'drafting', 'optimization']
            },
            'seo_config': self.input_manager.get_seo_config(),
            'status': 'completed'
        }
    
    def run(self, blog_input: BlogInput) -> Dict[str, Any]:
        """Esegue il processo completo di generazione del blog"""
        if not blog_input.validate():
            raise ValueError("Input non valido")
        
        logger.info(f"Avvio generazione blog per topic: {blog_input.topic}")
        start_time = datetime.now()
        
        try:
            # Setup agenti e task
            self.setup_agents(blog_input)
            self.setup_tasks(blog_input)
            
            # Crea crew
            crew = Crew(
                agents=list(self.agents.values()),
                tasks=list(self.tasks.values()),
                verbose=True
            )
            
            # Esegui generazione
            result = crew.kickoff(inputs=blog_input.to_dict())
            
            # Calcola tempo di esecuzione
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Genera analytics
            analytics = self.generate_analytics_report(blog_input, execution_time)
            
            logger.info(f"Generazione completata in {execution_time:.2f} secondi")
            
            return {
                'result': result,
                'analytics': analytics,
                'execution_time': execution_time
            }
            
        except Exception as e:
            logger.error(f"Errore durante la generazione: {e}")
            raise

def setup_argument_parser() -> argparse.ArgumentParser:
    """Configura il parser degli argomenti della command line"""
    parser = argparse.ArgumentParser(
        description="Blog Generator Enhanced - Genera articoli SEO ottimizzati",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi di utilizzo:

1. Modalità interattiva:
   python blog_generator_enhanced.py --interactive

2. Con parametri specifici:
   python blog_generator_enhanced.py --topic "Case Vacanza Costiera Amalfitana" 
   --intent commerciale --website "https://miosito.it" --business "Affitti turistici"

3. Da file di configurazione:
   python blog_generator_enhanced.py --input-file config_articolo.yaml

4. Genera template di input:
   python blog_generator_enhanced.py --generate-template
        """
    )
    
    # Opzioni principali
    parser.add_argument("--topic", type=str, help="Topic dell'articolo")
    parser.add_argument("--intent", choices=["informativo", "commerciale", "educativo"], 
                       default="informativo", help="Intento dell'articolo")
    parser.add_argument("--website", type=str, help="Sito web di destinazione")
    parser.add_argument("--business", type=str, help="Attività/servizio da sponsorizzare")
    parser.add_argument("--audience", type=str, default="pubblico generale", 
                       help="Pubblico target")
    parser.add_argument("--tone", choices=["professionale", "casual", "tecnico"], 
                       default="professionale", help="Tono di voce")
    parser.add_argument("--words", type=int, default=2000, help="Numero di parole target")
    
    # Opzioni modalità
    parser.add_argument("--interactive", action="store_true", 
                       help="Modalità interattiva per configurazione")
    parser.add_argument("--input-file", type=str, 
                       help="File YAML/JSON con configurazione completa")
    parser.add_argument("--generate-template", action="store_true",
                       help="Genera template di input")
    
    # Opzioni output
    parser.add_argument("--save", action="store_true", default=True,
                       help="Salva risultato in file markdown")
    parser.add_argument("--output-dir", type=str, default=".",
                       help="Directory di output")
    parser.add_argument("--config", type=str, default="config.yaml",
                       help="File di configurazione")
    
    return parser

def main():
    """Funzione principale"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    try:
        # Inizializza il generatore
        generator = BlogGeneratorEnhanced(
            config_path=args.config,
            prompts_path="prompts.yaml"
        )
        
        # Genera template se richiesto
        if args.generate_template:
            generator.input_manager.save_input_template()
            print("Template di input generato: input_template.yaml")
            return
        
        # Crea input in base alla modalità
        if args.interactive:
            blog_input = generator.input_manager.create_input_interactive()
        elif args.input_file:
            blog_input = generator.input_manager.create_input_from_file(args.input_file)
        else:
            blog_input = generator.input_manager.create_input_from_args(args)
            if not blog_input.topic:
                blog_input.topic = "Case Vacanza in Costiera Amalfitana 2025"  # Default
        
        # Esegui generazione
        logger.info("Avvio processo di generazione...")
        result_data = generator.run(blog_input)
        
        # Salva risultato
        if args.save:
            filename = generator.save_final_result(result_data['result'], blog_input)
            print(f"\n✅ Articolo generato e salvato in: {filename}")
            
            # Salva analytics se abilitato
            if result_data['analytics']:
                analytics_file = filename.replace('.md', '_analytics.json')
                with open(analytics_file, 'w', encoding='utf-8') as f:
                    json.dump(result_data['analytics'], f, indent=2, ensure_ascii=False)
                print(f"📊 Report analytics salvato in: {analytics_file}")
        else:
            print("\n" + "="*50)
            print("RISULTATO FINALE:")
            print("="*50)
            print(result_data['result'])
        
        print(f"\n⏱️  Tempo di esecuzione: {result_data['execution_time']:.2f} secondi")
        
    except KeyboardInterrupt:
        logger.info("Processo interrotto dall'utente")
    except Exception as e:
        logger.error(f"Errore durante l'esecuzione: {e}")
        raise

if __name__ == "__main__":
    main()
