import requests
from bs4 import BeautifulSoup

class ResponseGetter:
    def __init__(self, url):
        self.url = url

    def get_response(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(self.url, headers=headers)
        
        if response.status_code == 200:
            return response
        else:
            return None

class CompanyInfoExtractor:
    def __init__(self, soup):
        self.soup = soup

    def extract(self):
        company_element = self.soup.find("div", id="u20")
        if company_element:
            company_name = company_element.get_text(strip=True)
            cnpj_element = company_element.find_next("div", class_="text")
            cnpj = cnpj_element.get_text(strip=True).split(":")[-1].strip()
            address_elements = company_element.find_all_next("div", class_="text")
            address = ", ".join([element.get_text(strip=True) for element in address_elements[1:]])

            company_name = company_name.replace('\n', '').replace('\t', '')
            address = address.replace('\n', '').replace('\t', '')

            return {
                "Nome da Empresa": company_name,
                "CNPJ": cnpj,
                "Endereço": address
            }
        else:
            return {}

class PaymentInfoExtractor:
    def __init__(self, soup):
        self.soup = soup

    def extract(self):
        payment_data = {}
        payment_element = self.soup.find("div", id="linhaForma")
        if payment_element:
            form_of_payment_label = payment_element.find("label", class_="txtMax2")
            form_of_payment = form_of_payment_label.find_next("label").get_text(strip=True)
            value_paid_element = payment_element.find_next("div", id="linhaTotal")
            value_paid = value_paid_element.find("span", class_="totalNumb").get_text(strip=True)

            payment_data["Forma de pagamento"] = form_of_payment
            payment_data["Valor total pago"] = value_paid

        return payment_data

class ItemsInfoExtractor:
    def __init__(self, soup):
        self.soup = soup

    def extract(self):
        data = []
        item_elements = self.soup.find_all("tr", id=lambda value: value and value.startswith("Item"))
        for item_element in item_elements:
            item_data = {}
            columns = item_element.find_all("td")
            product_info = columns[0].get_text(strip=True)
            product_name = product_info.split("(")[0].strip()
            item_data["Produto"] = product_name
            item_data["Qtde"] = product_info.split("Qtde.:")[1].split("UN:")[0]
            item_data["UN"] = product_info.split("UN:")[1].split("Vl. Unit.:")[0]
            item_data["Vl. Unit."] = product_info.split("Vl. Unit.:")[1]
            total_value = columns[1].get_text(strip=True)
            item_data["Vl. Total"] = total_value.replace("Vl. Total", "")
            data.append(item_data)

        return data

class NotaFiscalExtractor:
    def __init__(self, url):
        self.url = url

    def extract(self):
        response_getter = ResponseGetter(self.url)
        response = response_getter.get_response()
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            company_info_extractor = CompanyInfoExtractor(soup)
            company_data = company_info_extractor.extract()
            
            payment_info_extractor = PaymentInfoExtractor(soup)
            payment_data = payment_info_extractor.extract()
            
            items_info_extractor = ItemsInfoExtractor(soup)
            items_data = items_info_extractor.extract()

            combined_data = {
                "Empresa": company_data,
                "Itens": items_data,
                "Informações de Pagamento": payment_data
            }
            return combined_data
        else:
            print("Não foi possível obter o conteúdo da página.")
