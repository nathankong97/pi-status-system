from db_models import Airline

class AirportSchedule_Helpers:
    def setValueforDestinationIATA(self, flight):
        try:
            return flight["flight"]["airport"]["destination"]["code"]["iata"]
        except:
            return "-"

    def setValueforCountry(self, flight):
        try:
            return flight["flight"]["airport"]["destination"]["position"]["country"]["name"]
        except:
            return "-"

    def setValueforCountryCode(self, flight):
        try:
            return flight["flight"]["airport"]["destination"]["position"]["country"]["code"]
        except:
            return "-"

    def setValueforDestinationAirport(self, flight):
        try:
            return flight["flight"]["airport"]["destination"]["name"]
        except:
            return "-"

    def setValueforCity(self, flight):
        try:
            return flight["flight"]["airport"]["destination"]["position"]["region"]["city"]
        except:
            return "-"

    def setValueforAirline(self, flight):
        try:
            iata = flight["flight"]["airline"]["code"]["iata"]
            icao = flight["flight"]["airline"]["code"]["icao"]
            airlineName = None
            if iata and icao:
                if iata == "JL":
                    airlineName = Airline(IATA=iata).name
                else:
                    airlineName = Airline(IATA=iata, ICAO=icao).name
            elif iata and not icao:
                airlineName = Airline(IATA=iata).name
            elif icao and not iata:
                airlineName = Airline(ICAO=icao).name
            if not airlineName:
                return flight["flight"]["airline"]["name"]
            return airlineName
        except:
            return "-"

    def setValueforAirlineIATA(self, flight):
        try:
            return flight["flight"]["airline"]["code"]["iata"]
        except:
            return "-"

    def setValueforAircraft(self, flight):
        try:
            return flight["flight"]["aircraft"]["model"]["code"]
        except:
            return "-"