import pandas as pd
import PyPDF2
import re
from typing import List, Dict, Optional, Tuple

class CAENDataProcessor:
    def __init__(self):
        self.rev2_to_rev3 = {}  # Now will store lists of corresponding codes
        self.rev3_details = {}
        self.activities_df = None
        self.sections = []
        self.initialize_sections()
        self.initialize_sample_data()

    def initialize_sections(self):
        """Initialize the sections for structured category display"""
        self.sections = [
            "A - AGRICULTURĂ, SILVICULTURĂ ȘI PESCUIT",
            "B - INDUSTRIA EXTRACTIVĂ",
            "C - INDUSTRIA PRELUCRĂTOARE",
            "D - PRODUCȚIA ȘI FURNIZAREA DE ENERGIE",
            "E - DISTRIBUȚIA APEI ȘI SALUBRITATE",
            "F - CONSTRUCȚII",
            "G - COMERȚ",
            "H - TRANSPORT ȘI DEPOZITARE",
            "I - HOTELURI ȘI RESTAURANTE",
            "J - INFORMAȚII ȘI COMUNICAȚII",
            "K - INTERMEDIERI FINANCIARE ȘI ASIGURĂRI",
            "L - TRANZACȚII IMOBILIARE",
            "M - ACTIVITĂȚI PROFESIONALE, ȘTIINȚIFICE ȘI TEHNICE",
            "N - SERVICII ADMINISTRATIVE",
            "O - ADMINISTRAȚIE PUBLICĂ",
            "P - ÎNVĂȚĂMÂNT",
            "Q - SĂNĂTATE ȘI ASISTENȚĂ SOCIALĂ",
            "R - ARTĂ, CULTURĂ ȘI RECREERE",
            "S - ALTE ACTIVITĂȚI DE SERVICII"
        ]

    def initialize_sample_data(self):
        """Initialize sample data for each section"""
        self.sample_activities = {
            'A': [
                {'rev2_code': '0111', 'rev3_code': '0111', 'description': 'Cultivarea cerealelor, plantelor leguminoase și a plantelor producătoare de semințe oleaginoase'},
                {'rev2_code': '0113', 'rev3_code': '0113', 'description': 'Cultivarea legumelor și a pepenilor, a rădăcinoaselor și tuberculilor'},
                {'rev2_code': '0116', 'rev3_code': '0116', 'description': 'Cultivarea plantelor pentru fibre textile'},
                {'rev2_code': '0121', 'rev3_code': '0121', 'description': 'Cultivarea strugurilor'},
                {'rev2_code': '0124', 'rev3_code': '0124', 'description': 'Cultivarea fructelor semintoase și sâmburoase'},
                {'rev2_code': '0141', 'rev3_code': '0141', 'description': 'Creșterea bovinelor de lapte'},
                {'rev2_code': '0145', 'rev3_code': '0145', 'description': 'Creșterea ovinelor și caprinelor'},
                {'rev2_code': '0146', 'rev3_code': '0146', 'description': 'Creșterea porcinelor'},
                {'rev2_code': '0147', 'rev3_code': '0147', 'description': 'Creșterea păsărilor'}
            ],
            'B': [
                {'rev2_code': '0510', 'rev3_code': '0510', 'description': 'Extracția cărbunelui superior'},
                {'rev2_code': '0520', 'rev3_code': '0520', 'description': 'Extracția cărbunelui inferior'},
                {'rev2_code': '0610', 'rev3_code': '0610', 'description': 'Extracția petrolului brut'},
                {'rev2_code': '0620', 'rev3_code': '0620', 'description': 'Extracția gazelor naturale'},
                {'rev2_code': '0710', 'rev3_code': '0710', 'description': 'Extracția minereurilor feroase'},
                {'rev2_code': '0729', 'rev3_code': '0729', 'description': 'Extracția altor minereuri metalifere neferoase'},
                {'rev2_code': '0811', 'rev3_code': '0811', 'description': 'Extracția pietrei ornamentale și a pietrei pentru construcții'}
            ],
            'C': [
                {'rev2_code': '1011', 'rev3_code': '1011', 'description': 'Prelucrarea și conservarea cărnii'},
                {'rev2_code': '1013', 'rev3_code': '1013', 'description': 'Fabricarea produselor din carne'},
                {'rev2_code': '1032', 'rev3_code': '1032', 'description': 'Fabricarea sucurilor de fructe și legume'},
                {'rev2_code': '1051', 'rev3_code': '1051', 'description': 'Fabricarea produselor lactate și a brânzeturilor'},
                {'rev2_code': '1071', 'rev3_code': '1071', 'description': 'Fabricarea pâinii; fabricarea prăjiturilor și a produselor proaspete de patiserie'},
                {'rev2_code': '1082', 'rev3_code': '1082', 'description': 'Fabricarea produselor din cacao, a ciocolatei și a produselor zaharoase'},
                {'rev2_code': '1102', 'rev3_code': '1102', 'description': 'Fabricarea vinurilor din struguri'},
                {'rev2_code': '1413', 'rev3_code': '1413', 'description': 'Fabricarea altor articole de îmbrăcăminte'},
                {'rev2_code': '1520', 'rev3_code': '1520', 'description': 'Fabricarea încălțămintei'}
            ],
            'G': [
                {'rev2_code': '4511', 'rev3_code': '4511', 'description': 'Comerț cu autoturisme și autovehicule ușoare'},
                {'rev2_code': '4520', 'rev3_code': '4520', 'description': 'Întreținerea și repararea autovehiculelor'},
                {'rev2_code': '4531', 'rev3_code': '4531', 'description': 'Comerț cu ridicata de piese și accesorii pentru autovehicule'},
                {'rev2_code': '4711', 'rev3_code': '4711', 'description': 'Comerț cu amănuntul în magazine nespecializate, cu vânzare predominantă de produse alimentare, băuturi și tutun'},
                {'rev2_code': '4721', 'rev3_code': '4721', 'description': 'Comerț cu amănuntul al fructelor și legumelor proaspete'},
                {'rev2_code': '4773', 'rev3_code': '4773', 'description': 'Comerț cu amănuntul al produselor farmaceutice'},
                {'rev2_code': '4776', 'rev3_code': '4776', 'description': 'Comerț cu amănuntul al florilor, plantelor și semințelor'}
            ],
            'I': [
                {'rev2_code': '5510', 'rev3_code': '5510', 'description': 'Hoteluri și alte facilități de cazare similare'},
                {'rev2_code': '5520', 'rev3_code': '5520', 'description': 'Facilități de cazare pentru vacanțe și perioade de scurtă durată'},
                {'rev2_code': '5590', 'rev3_code': '5590', 'description': 'Alte servicii de cazare'},
                {'rev2_code': '5610', 'rev3_code': '5610', 'description': 'Restaurante'},
                {'rev2_code': '5621', 'rev3_code': '5621', 'description': 'Activități de alimentație (catering) pentru evenimente'},
                {'rev2_code': '5630', 'rev3_code': '5630', 'description': 'Baruri și alte activități de servire a băuturilor'}
            ],
            'J': [
                {'rev2_code': '5811', 'rev3_code': '5811', 'description': 'Activități de editare a cărților'},
                {'rev2_code': '5813', 'rev3_code': '5813', 'description': 'Activități de editare a ziarelor'},
                {'rev2_code': '5911', 'rev3_code': '5911', 'description': 'Activități de producție cinematografică, video și de programe de televiziune'},
                {'rev2_code': '6201', 'rev3_code': '6201', 'description': 'Activități de realizare a soft-ului la comandă'},
                {'rev2_code': '6202', 'rev3_code': '6202', 'description': 'Activități de consultanță în tehnologia informației'},
                {'rev2_code': '6209', 'rev3_code': '6209', 'description': 'Alte activități de servicii privind tehnologia informației'},
                {'rev2_code': '6311', 'rev3_code': '6311', 'description': 'Prelucrarea datelor, administrarea paginilor web și activități conexe'}
            ],
            'K': [
                {'rev2_code': '6419', 'rev3_code': '6419', 'description': 'Alte activități de intermedieri monetare'},
                {'rev2_code': '6492', 'rev3_code': '6492', 'description': 'Alte activități de creditare'},
                {'rev2_code': '6511', 'rev3_code': '6511', 'description': 'Activități de asigurări de viață'},
                {'rev2_code': '6512', 'rev3_code': '6512', 'description': 'Alte activități de asigurări (exceptând asigurările de viață)'},
                {'rev2_code': '6612', 'rev3_code': '6612', 'description': 'Activități de intermediere a tranzacțiilor financiare'},
                {'rev2_code': '6619', 'rev3_code': '6619', 'description': 'Activități auxiliare intermedierilor financiare'}
            ],
            'L': [
                {'rev2_code': '6810', 'rev3_code': '6810', 'description': 'Cumpărarea și vânzarea de bunuri imobiliare proprii'},
                {'rev2_code': '6820', 'rev3_code': '6820', 'description': 'Închirierea și subînchirierea bunurilor imobiliare proprii sau închiriate'},
                {'rev2_code': '6831', 'rev3_code': '6831', 'description': 'Agenții imobiliare'},
                {'rev2_code': '6832', 'rev3_code': '6832', 'description': 'Administrarea imobilelor pe bază de comision sau contract'}
            ],
            'M': [
                {'rev2_code': '6910', 'rev3_code': '6910', 'description': 'Activități juridice'},
                {'rev2_code': '6920', 'rev3_code': '6920', 'description': 'Activități de contabilitate și audit financiar; consultanță în domeniul fiscal'},
                {'rev2_code': '7111', 'rev3_code': '7111', 'description': 'Activități de arhitectură'},
                {'rev2_code': '7112', 'rev3_code': '7112', 'description': 'Activități de inginerie și consultanță tehnică legate de acestea'},
                {'rev2_code': '7220', 'rev3_code': '7220', 'description': 'Cercetare-dezvoltare în științe sociale și umaniste'},
                {'rev2_code': '7311', 'rev3_code': '7311', 'description': 'Activități ale agențiilor de publicitate'},
                {'rev2_code': '7420', 'rev3_code': '7420', 'description': 'Activități fotografice'}
            ],
            'N': [
                {'rev2_code': '7711', 'rev3_code': '7711', 'description': 'Activități de închiriere și leasing cu autoturisme și autovehicule rutiere ușoare'},
                {'rev2_code': '7721', 'rev3_code': '7721', 'description': 'Activități de închiriere și leasing cu bunuri recreaționale și echipament sportiv'},
                {'rev2_code': '7810', 'rev3_code': '7810', 'description': 'Activități ale agențiilor de plasare a forței de muncă'},
                {'rev2_code': '7911', 'rev3_code': '7911', 'description': 'Activități ale agențiilor turistice'},
                {'rev2_code': '8020', 'rev3_code': '8020', 'description': 'Activități de servicii privind sistemele de securizare'},
                {'rev2_code': '8121', 'rev3_code': '8121', 'description': 'Activități generale de curățenie a clădirilor'},
                {'rev2_code': '8130', 'rev3_code': '8130', 'description': 'Activități de întreținere peisagistică'}
            ],
            'O': [
                {'rev2_code': '8411', 'rev3_code': '8411', 'description': 'Servicii de administrație publică generală'},
                {'rev2_code': '8412', 'rev3_code': '8412', 'description': 'Reglementarea activităților organismelor care prestează servicii în domeniul îngrijirii sănătății, învățământului, culturii și al altor activități sociale, exclusiv protecția socială'},
                {'rev2_code': '8422', 'rev3_code': '8422', 'description': 'Activități de apărare națională'},
                {'rev2_code': '8423', 'rev3_code': '8423', 'description': 'Activități de justiție'},
                {'rev2_code': '8424', 'rev3_code': '8424', 'description': 'Activități de ordine publică și de protecție civilă'}
            ],
            'P': [
                {'rev2_code': '8510', 'rev3_code': '8510', 'description': 'Învățământ preșcolar'},
                {'rev2_code': '8520', 'rev3_code': '8520', 'description': 'Învățământ primar'},
                {'rev2_code': '8531', 'rev3_code': '8531', 'description': 'Învățământ secundar general'},
                {'rev2_code': '8532', 'rev3_code': '8532', 'description': 'Învățământ secundar, tehnic sau profesional'},
                {'rev2_code': '8541', 'rev3_code': '8541', 'description': 'Învățământ superior non-universitar'},
                {'rev2_code': '8542', 'rev3_code': '8542', 'description': 'Învățământ superior universitar'},
                {'rev2_code': '8551', 'rev3_code': '8551', 'description': 'Învățământ în domeniul sportiv și recreational'}
            ],
            'Q': [
                {'rev2_code': '8610', 'rev3_code': '8610', 'description': 'Activități de asistență spitalicească'},
                {'rev2_code': '8621', 'rev3_code': '8621', 'description': 'Activități de asistență medicală generală'},
                {'rev2_code': '8622', 'rev3_code': '8622', 'description': 'Activități de asistență medicală specializată'},
                {'rev2_code': '8623', 'rev3_code': '8623', 'description': 'Activități de asistență stomatologică'},
                {'rev2_code': '8690', 'rev3_code': '8690', 'description': 'Alte activități referitoare la sănătatea umană'},
                {'rev2_code': '8710', 'rev3_code': '8710', 'description': 'Activități ale centrelor de îngrijire medicală'},
                {'rev2_code': '8891', 'rev3_code': '8891', 'description': 'Activități de îngrijire zilnică pentru copii'}
            ],
            'R': [
                {'rev2_code': '9001', 'rev3_code': '9001', 'description': 'Activități de interpretare artistică (spectacole)'},
                {'rev2_code': '9002', 'rev3_code': '9002', 'description': 'Activități suport pentru interpretarea artistică (spectacole)'},
                {'rev2_code': '9101', 'rev3_code': '9101', 'description': 'Activități ale bibliotecilor și arhivelor'},
                {'rev2_code': '9102', 'rev3_code': '9102', 'description': 'Activități ale muzeelor'},
                {'rev2_code': '9103', 'rev3_code': '9103', 'description': 'Gestionarea monumentelor, clădirilor istorice și a altor obiective de interes turistic'},
                {'rev2_code': '9311', 'rev3_code': '9311', 'description': 'Activități ale bazelor sportive'},
                {'rev2_code': '9313', 'rev3_code': '9313', 'description': 'Activități ale centrelor de fitness'}
            ],
            'S': [
                {'rev2_code': '9511', 'rev3_code': '9511', 'description': 'Repararea calculatoarelor și a echipamentelor periferice'},
                {'rev2_code': '9512', 'rev3_code': '9512', 'description': 'Repararea echipamentelor de comunicații'},
                {'rev2_code': '9521', 'rev3_code': '9521', 'description': 'Repararea aparatelor electronice de uz casnic'},
                {'rev2_code': '9522', 'rev3_code': '9522', 'description': 'Repararea dispozitivelor de uz gospodăresc și a echipamentelor pentru casă și grădină'},
                {'rev2_code': '9601', 'rev3_code': '9601', 'description': 'Spălarea și curățarea (uscată) articolelor textile și a produselor din blană'},
                {'rev2_code': '9602', 'rev3_code': '9602', 'description': 'Coafură și alte activități de înfrumusețare'},
                {'rev2_code': '9603', 'rev3_code': '9603', 'description': 'Activități de pompe funebre și similare'}
            ]
        }

    def get_categories(self) -> List[str]:
        """Get list of sections for organized category display"""
        return self.sections

    def search_activities(self, 
                       keyword: Optional[str] = None,
                       category: Optional[str] = None) -> List[Dict]:
        """
        Search activities with filters for keywords and categories
        """
        try:
            results = []

            # If category is selected, get activities for that section
            if category:
                section_letter = category.split(' - ')[0].strip()
                if section_letter in self.sample_activities:
                    results = self.sample_activities[section_letter]

                # If keyword is also provided, filter the results
                if keyword and results:
                    results = [
                        item for item in results 
                        if (keyword.lower() in item['description'].lower() or
                            keyword in item['rev2_code'] or
                            keyword in item['rev3_code'])
                    ]

            # If only keyword is provided
            elif keyword:
                # Search across all sections
                for activities in self.sample_activities.values():
                    for item in activities:
                        if (keyword.lower() in item['description'].lower() or
                            keyword in item['rev2_code'] or
                            keyword in item['rev3_code']):
                            results.append(item)

            return results

        except Exception as e:
            print(f"Error in search_activities: {str(e)}")
            return []

    def extract_correspondence_data(self, pdf_path):
        """Extract CAEN Rev.2 to Rev.3 correspondence data, handling multiple mappings"""
        correspondence_data = {}

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page in pdf_reader.pages:
                    text = page.extract_text()
                    # Look for patterns like "1234 → 5678, 9012" or "1234 → 5678; 9012"
                    # Also handle cases without arrows like "1234 5678, 9012"
                    matches = re.finditer(r'(\d{4})\s*(?:→|->|\s+)(\d{4}(?:[,;\s]+\d{4})*)', text)

                    for match in matches:
                        rev2_code = match.group(1)
                        # Extract all 4-digit codes from the second group
                        rev3_codes = re.findall(r'\d{4}', match.group(2))
                        print(f"Found mapping: {rev2_code} -> {rev3_codes}")  # Debug print
                        correspondence_data[rev2_code] = rev3_codes

        except Exception as e:
            print(f"Error in extract_correspondence_data: {str(e)}")
            return {}

        self.rev2_to_rev3 = correspondence_data
        print(f"Total mappings found: {len(correspondence_data)}")  # Debug print
        # Print some sample mappings
        sample_keys = list(correspondence_data.keys())[:5]
        for key in sample_keys:
            print(f"Sample mapping: {key} -> {correspondence_data[key]}")


    def extract_rev3_details(self, pdf_path):
        """Extract CAEN Rev.3 codes and their descriptions"""
        rev3_data = {}
        categories = {}
        current_category = None

        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                text = page.extract_text()
                lines = text.split('\n')

                for line in lines:
                    # Match category headers (divisions)
                    category_match = re.match(r'^(\d{2})\s+(.+)$', line.strip())
                    if category_match:
                        current_category = category_match.group(2)
                        continue

                    # Match CAEN codes and descriptions
                    code_match = re.match(r'^(\d{4})\s+(.+)$', line.strip())
                    if code_match and current_category:
                        code, description = code_match.groups()
                        rev3_data[code] = {
                            'description': description.strip(),
                            'category': current_category
                        }

        self.rev3_details = rev3_data
        self._create_dataframe()

    def _create_dataframe(self):
        """Create a DataFrame for efficient searching and filtering"""
        data = []
        for rev2_code, rev3_codes in self.rev2_to_rev3.items():
            for rev3_code in rev3_codes:
                if rev3_code in self.rev3_details:
                    data.append({
                        'rev2_code': rev2_code,
                        'rev3_code': rev3_code,
                        'description': self.rev3_details[rev3_code]['description'],
                        'category': self.rev3_details[rev3_code]['category']
                    })

        self.activities_df = pd.DataFrame(data)

    def get_conversion(self, rev2_code: str) -> List[Dict]:
        """Get conversion data for a Rev.2 code, returning all corresponding Rev.3 codes"""
        if rev2_code not in self.rev2_to_rev3:
            return []

        results = []
        rev3_codes = self.rev2_to_rev3[rev2_code]

        # Handle both single and multiple corresponding codes
        for rev3_code in rev3_codes:
            if rev3_code in self.rev3_details:
                results.append({
                    'rev2_code': rev2_code,
                    'rev3_code': rev3_code,
                    'description': self.rev3_details[rev3_code]['description'],
                    'category': self.rev3_details[rev3_code].get('category', '')
                })

        return results