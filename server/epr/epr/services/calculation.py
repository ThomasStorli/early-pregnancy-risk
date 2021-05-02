from ..services.complications import diabetes, preeclampsia, sptd, miscarriage, stillbirth, ppd, caesearean_delivery
from ..exceptions.api_exceptions import InternalServerError
from ..models import Translation, Complication_Risk

class Calculation:
    def __init__(self, json_dict: dict, language_code: str):
        self.language_code = language_code

        # Add multiple risks here
        self.diabetes = risk_dict_constructor("diabetes", diabetes.calculate(json_dict), language_code)
        self.preeclampsia = risk_dict_constructor("preeclampsia", preeclampsia.calculate(json_dict), language_code)
        self.spdt = risk_dict_constructor("spdt", sptd.calculate(json_dict), language_code)
        self.miscarriage = risk_dict_constructor("misscarriage", miscarriage.calculate(json_dict), language_code)
        self.stillbirth = risk_dict_constructor("stillbirth", stillbirth.calculate(json_dict), language_code)
        self.ppd = risk_dict_constructor("ppd", ppd.calculate(json_dict), language_code)
        self.caesearean_delivery = risk_dict_constructor("caesearean_delivery", caesearean_delivery.calculate(json_dict), language_code)


def risk_dict_constructor(complication: str, risk_results: dict, language_code: str) -> dict:
    translated_comp = Translation.objects.get(belongs_to__name=complication, language_code__code=language_code).text
    if translated_comp is None:
        translated_comp = Translation.objects.get(belongs_to=complication, language__code="en").text
    
    percentage_translated = Translation.objects.get(belongs_to__name="percentage_of_pregnancies", language_code__code=language_code).text

    percentage_risk = Complication_Risk.objects.get(related_complication__name=complication, severity = "{}".format(risk_results["severity"])).percentage


    return  {"complication" : translated_comp, "severity": risk_results["severity"], "risk_str":"{} {}".format(percentage_risk, percentage_translated), "risk_score": risk_results["risk"]}
