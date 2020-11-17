from models import Airport, Country

class General_Helpers:
    
    @staticmethod
    def getCountryCodeByIATA(IATA):
        countryName = Airport(IATA).country
        return Country(name=countryName).code.lower()