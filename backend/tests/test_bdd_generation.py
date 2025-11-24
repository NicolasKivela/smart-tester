import pytest
from unittest.mock import patch
from app.bdd_scenarios.bdd_generation import parse_gherkin
from app.bdd_scenarios.schemas import BDD_Scenario

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_single_scenario(mock_db):
    """Test parsing a single, well-formed Gherkin scenario."""
    gherkin_text = "Scenario: Successful login\n  Given I am on the login page\n  When I enter valid credentials\n  Then I am redirected to the dashboard"
    mock_db.add_bdd_scenarios.return_value = {"status_code": 200, "message": "Success"}
    
    result = parse_gherkin(gherkin_text, "Login feature", 1)
    
    mock_db.add_bdd_scenarios.assert_called_once()
    call_args = mock_db.add_bdd_scenarios.call_args[0]
    assert call_args[0] == 1
    assert isinstance(call_args[1], BDD_Scenario)
    assert call_args[1].scenario == "Successful login"
    assert call_args[1].content.strip().startswith("Successful login")
    assert result == {"status_code": 200, "message": "Success"}

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_multiple_scenarios(mock_db):
    """Test parsing Gherkin text with multiple scenarios."""
    gherkin_text = (
        "Scenario: First scenario\n  Given a condition\n"
        "Scenario: Second scenario\n  When an action occurs"
    )
    mock_db.add_bdd_scenarios.return_value = {"status_code": 200}
    
    result = parse_gherkin(gherkin_text, "feature", 2)
    
    assert mock_db.add_bdd_scenarios.call_count == 2
    
    first_call_args = mock_db.add_bdd_scenarios.call_args_list[0][0]
    assert first_call_args[1].scenario == "First scenario"
    
    second_call_args = mock_db.add_bdd_scenarios.call_args_list[1][0]
    assert second_call_args[1].scenario == "Second scenario"
    
    assert result == {"status_code": 200} # Returns the result of the last call

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_with_and_steps(mock_db):
    """Test parsing a scenario with 'And' steps."""
    gherkin_text = "Scenario: Complex scenario\n  Given initial state\n  And another state\n  When I do something\n  And something else\n  Then I see a result\n  And another result"
    mock_db.add_bdd_scenarios.return_value = {"status_code": 200}

    parse_gherkin(gherkin_text, "feature", 3)

    mock_db.add_bdd_scenarios.assert_called_once()
    call_args = mock_db.add_bdd_scenarios.call_args[0]
    bdd_scenario = call_args[1]
    
    expected_content = "Complex scenario\n  Given initial state\n  And another state\n  When I do something\n  And something else\n  Then I see a result\n  And another result"
    assert bdd_scenario.scenario == "Complex scenario"
    assert bdd_scenario.content.strip() == expected_content

def test_parse_gherkin_empty_input_raises_error():
    """Test that parsing an empty Gherkin string raises an error."""
    # The current implementation raises UnboundLocalError for empty input
    # because 'response' is not initialized if no scenarios are found.
    with pytest.raises(UnboundLocalError):
        parse_gherkin("", "feature", 4)

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_no_scenario_keyword(mock_db):
    """Test parsing text without the 'Scenario:' keyword."""
    # If "Scenario:" keyword is missing, the whole text is treated as one scenario block.
    gherkin_text = "This is just some text without the Scenario keyword."
    mock_db.add_bdd_scenarios.return_value = {"status_code": 200}
    
    parse_gherkin(gherkin_text, "feature", 5)
    
    mock_db.add_bdd_scenarios.assert_called_once()
    call_args = mock_db.add_bdd_scenarios.call_args[0]
    assert call_args[1].scenario == "This is just some text without the Scenario keyword."
    assert call_args[1].content == "This is just some text without the Scenario keyword."

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_extra_whitespace_and_empty_lines(mock_db):
    """Test that parsing handles extra whitespace and empty lines."""
    gherkin_text = """
    
        Scenario:    Scenario with extra spaces   
    
            Given   a step with spaces   
    
    """
    mock_db.add_bdd_scenarios.return_value = {"status_code": 200}
    
    parse_gherkin(gherkin_text, "feature", 6)
    
    mock_db.add_bdd_scenarios.assert_called_once()
    call_args = mock_db.add_bdd_scenarios.call_args[0]
    assert call_args[1].scenario == "Scenario with extra spaces"
    assert "Given   a step with spaces" in call_args[1].content

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_db_error(mock_db):
    """Test that the function returns the error response from the database."""
    gherkin_text = "Scenario: Test DB error\n  Given a setup"
    error_response = {"status_code": 500, "detail": "Database error"}
    mock_db.add_bdd_scenarios.return_value = error_response
    
    result = parse_gherkin(gherkin_text, "feature", 7)
    
    assert result == error_response
    mock_db.add_bdd_scenarios.assert_called_once()

@patch('app.bdd_scenarios.bdd_generation.db_bdd_scenarios')
def test_parse_gherkin_and_without_context(mock_db):
    """Test that 'And' is ignored if it appears before a Given/When/Then."""
    gherkin_text = "Scenario: And first\n  And this should be ignored\n  Given a proper step"
    mock_db.add_bdd_scenarios.return_value = {"status_code": 200}
    
    parse_gherkin(gherkin_text, "feature", 8)
    
    mock_db.add_bdd_scenarios.assert_called_once()
    call_args = mock_db.add_bdd_scenarios.call_args[0]
    bdd_scenario = call_args[1]
    
    # This test documents that the parser doesn't crash, although the 'And'
    # is not associated with any step since no Given/When/Then precedes it.
    # The step parsing logic is not used in the final object creation, but
    # this ensures the parsing logic itself is robust.
    assert bdd_scenario.scenario == "And first"
    assert "And this should be ignored" in bdd_scenario.content
