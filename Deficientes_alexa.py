from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response, Intent
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_model.dialog import ElicitSlotDirective
import pymysql.cursors

sb = SkillBuilder()


connection = pymysql.connect(
    host="localhost",
    user="root",
    passwd="",
    database="deficientes_projeto"
    )

cursor = connection.cursor()

class Handler(object):
    """Implementa funções compartilhadas entre classes"""
    def can_handle(self, handler_input, nome):
        """return a boolean value depending on the type"""
        # type: (HandlerInput) -> bool
        if "request" in nome.lower():
            return is_request_type(nome)(handler_input)
        elif "intent" in nome.lower():
            return is_intent_type(nome)(handler_input)
            raise Exception("Nome do Handler inválido!")

    #   aaaa
    def handle(self, handler_input, speech_text):
        """Handles the given alexa inputs"""
        
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here
        if speech_text:
            handler_input.response_builder.speak(speech_text).set_card(
                SimpleCard("Hello World", speech_text)).set_should_end_session(
                False)
            #Retorna resposta
            return handler_input.response_builder.response




class LaunchRequestHandler(AbstractRequestHandler, Handler):
    can_handle(self, handler_input, __class__.__name__)
    handle(self, handler_input, "Skill em desenvolvimento"):

class OpcaoUmIntentHandler(AbstractRequestHandler, Handler):
    can_handle(self, handler_input, __class__.__name__)

    slots = handler_input.request_envelope.request.intent.slots
    nome = slots["Rua"].value
    speak_output = f"O nome da \"{nome}\" foi adicionado com sucesso."

    #Resposta da alexa
    handle(self, handler_input, speak_output):

    #Insere no DB
    comando_SQL = "INSERT INTO lugar (rua) VALUES (%s)"
    cursor.execute(comando_SQL, (nome))
    connection.commit()

    return handler_input.response_builder.response


class OpcaoDoisIntentHandler(AbstractRequestHandler, Handler):
    can_handle(self, handler_input, __class__.__name__)
    
    #Sobrescreve a função handle da classe mãe
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        comando_SQL = "SELECT * FROM lugar"
        cursor.execute(comando_SQL)
        valores_lidos = cursor.fetchall()
        lista = []

        for c in valores_lidos:
            lista.append(c)

            values = ' '.join(str(v) for v in lista)

            handler_input.response_builder.speak(values).set_card(
                SimpleCard("Hello World", values)).set_should_end_session(
                True)
        # Retorna
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler, Handler):
    #Sobrescreve a função da classe mãe
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(
            handler_input)
    handle(self, handler_input, "Cancelado!")


class SessionEndedRequestHandler(AbstractRequestHandler, Handler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    handle(self, handler_input, "Goodbye!")


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(OpcaoUmIntentHandler())
sb.add_request_handler(OpcaoDoisIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
