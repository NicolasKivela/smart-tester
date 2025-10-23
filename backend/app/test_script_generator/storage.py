import json
from app.test_script_generator.schemas import test_script
#temporary storage later BD
TEST_SCRIPTS = {
    1: test_script(
        id=1,
        feature_id=1,
        bdd_ids=[1, 2, 3],
        script_code="Code here",
        keywords=["ekw", "ekek"]
    )
}


class db_test_scripts():
    def save_keywords(id):
        return
    def get_keywords():
        return
    def save_testscript(id, feature_id, bdd_scenarios,script_code):
        try:
            script_code = json.loads(script_code)
            bdd_ids = []
            for bdd in bdd_scenarios:
                bdd_ids.append(bdd.get("id"))
            TEST_SCRIPTS[id] = test_script(id=id,feature_id=feature_id,
                                       bdd_ids=bdd_ids, script_code=script_code["test_script"]
                                       )
            return "Succesfully saved test script object"
        except Exception as e:
            print(f"error {e}")
            print(f"Error saving testscript id:{id}")  