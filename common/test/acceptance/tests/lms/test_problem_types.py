import textwrap
import random

from ...fixtures.course import XBlockFixtureDesc
from ...pages.lms.problem import ProblemPage
from .test_lms_problems import ProblemsTest
from ..helpers import select_option_by_text

from capa.tests.response_xml_factory import (
    ChoiceResponseXMLFactory,
    ChoiceTextResponseXMLFactory,
    CodeResponseXMLFactory,
    CustomResponseXMLFactory,
    FormulaResponseXMLFactory,
    ImageResponseXMLFactory,
    MultipleChoiceResponseXMLFactory,
    NumericalResponseXMLFactory,
    OptionResponseXMLFactory,
    StringResponseXMLFactory,
)

class ProblemTypeTest(ProblemsTest):
    problem_name = None
    problem_type = None
    factory = None
    factory_kwargs = {}
    status_indicators = {
        'correct': ['span.correct'],
        'incorrect': ['span.incorrect'],
        'unanswered': ['span.unanswered'],
    }

    def setUp(self):
        super(ProblemTypeTest, self).setUp()
        self.courseware_page.visit()
        self.problem_page = ProblemPage(self.browser)

    def get_problem(self):
        """
        Create a checkbox problem
        """
        # Generate the problem XML using capa.tests.response_xml_factory
        return XBlockFixtureDesc(
            'problem',
            self.problem_name,
            data=self.factory.build_xml(**self.factory_kwargs),
            metadata={'rerandomize': 'always'}
        )

    def wait_for_status(self, status):
        msg = "Wait for status to be {}".format(status)
        for status_indicator in self.status_indicators[status]:
            self.problem_page.wait_for_element_visibility(status_indicator, msg)


class ProblemTypeTestMixin(object):
    def test_answer_correctly(self):
        """
        Scenario: I can answer a problem correctly
        Given External graders respond "correct"
        And I am viewing a "<ProblemType>" problem
        When I answer a "<ProblemType>" problem "correctly"
        Then my "<ProblemType>" answer is marked "correct"
        And The "<ProblemType>" problem displays a "correct" answer
        And a "problem_check" server event is emitted
        And a "problem_check" browser event is emitted
        """
        # Make sure we're looking at the right problem
        self.assertEqual(self.problem_page.problem_name, self.problem_name)

        # Answer the problem correctly
        self.answer_problem(True)
        self.problem_page.click_check()
        self.wait_for_status('correct')
        # TODO: check events emitted



class CheckboxProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'CHECKBOX TEST PROBLEM'
    problem_type = 'checkbox'

    factory = ChoiceResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The correct answer is Choice 3',
        'choice_type': 'checkbox',
        'choices': [True, False, True, False],
        'choice_names': ['Choice 0', 'Choice 1', 'Choice 2', 'Choice 3']
    }

    def answer_problem(self, correct):
        """
        Answer checkbox problem.
        """
        if correct:
            self.problem_page.click_choice("choice_0")
            self.problem_page.click_choice("choice_2")
        else:
            self.problem_page.click_choice("choice_1")

class MultipleChoiceProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'MULTIPLE CHOICE TEST PROBLEM'
    problem_type = 'multiple choice'

    factory = MultipleChoiceResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The correct answer is Choice 2',
        'choices': [False, False, True, False],
        'choice_names': ['choice_0', 'choice_1', 'choice_2', 'choice_3'],
    }
    status_indicators = {
        'correct': ['label.choicegroup_correct'],
        'incorrect': ['label.choicegroup_incorrect', 'span.incorrect'],
        'unanswered': ['span.unanswered'],
    }

    def answer_problem(self, correct):
        """
        Answer multiple choice problem.
        """
        if correct:
            self.problem_page.click_choice("choice_choice_2")
        else:
            self.problem_page.click_choice("choice_choice_1")


class RadioProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'RADIO TEST PROBLEM'
    problem_type = 'radio'

    factory = ChoiceResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The correct answer is Choice 2',
        'choice_type': 'radio',
        'choices': [False, False, True, False],
        'choice_names': ['Choice 0', 'Choice 1', 'Choice 2', 'Choice 3'],
    }
    status_indicators = {
        'correct': ['label.choicegroup_correct'],
        'incorrect': ['label.choicegroup_incorrect', 'span.incorrect'],
        'unanswered': ['span.unanswered'],
    }

    def answer_problem(self, correct):
        """
        Answer radio problem.
        """
        if correct:
            self.problem_page.click_choice("choice_2")
        else:
            self.problem_page.click_choice("choice_1")


class DropDownProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'DROP DOWN TEST PROBLEM'
    problem_type = 'drop down'

    factory = OptionResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The correct answer is Option 2',
        'options': ['Option 1', 'Option 2', 'Option 3', 'Option 4'],
        'correct_option': 'Option 2'
    }

    def answer_problem(self, correct):
        """
        Answer drop down problem.
        """
        answer = 'Option 2' if correct else 'Option 3'
        selector_element = self.problem_page.q(css='.problem .option-input select')
        select_option_by_text(selector_element, answer)


class StringProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'STRING TEST PROBLEM'
    problem_type = 'string'

    factory = StringResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The answer is "correct string"',
        'case_sensitive': False,
        'answer': 'correct string',
    }

    status_indicators = {
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered', 'div.unsubmitted'],
    }

    def answer_problem(self, correct):
        """
        Answer string problem.
        """
        textvalue = 'correct string' if correct else 'incorrect string'
        self.problem_page.fill_answer(textvalue)


class NumericalProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'NUMERICAL TEST PROBLEM'
    problem_type = 'numerical'

    factory = NumericalResponseXMLFactory()

    factory_kwargs =  {
        'question_text': 'The answer is pi + 1',
        'answer': '4.14159',
        'tolerance': '0.00001',
        'math_display': True,
    }

    status_indicators = {
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered', 'div.unsubmitted'],
    }

    def answer_problem(self, correct):
        """
        Answer numerical problem.
        """
        textvalue = "pi + 1" if correct else str(random.randint(-2, 2))
        self.problem_page.fill_answer(textvalue)


class FormulaProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'FORMULA TEST PROBLEM'
    problem_type = 'formula'

    factory = FormulaResponseXMLFactory()

    factory_kwargs =  {
        'question_text': 'The solution is [mathjax]x^2+2x+y[/mathjax]',
        'sample_dict': {'x': (-100, 100), 'y': (-100, 100)},
        'num_samples': 10,
        'tolerance': 0.00001,
        'math_display': True,
        'answer': 'x^2+2*x+y',
    }

    status_indicators = {
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered', 'div.unsubmitted'],
    }

    def answer_problem(self, correct):
        """
        Answer formula problem.
        """
        textvalue = "x^2+2*x+y" if correct else 'x^2'
        self.problem_page.fill_answer(textvalue)


class ScriptProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'SCRIPT TEST PROBLEM'
    problem_type = 'script'

    factory = CustomResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'Enter two integers that sum to 10.',
        'cfn': 'test_add_to_ten',
        'expect': '10',
        'num_inputs': 2,
        'script': textwrap.dedent("""
            def test_add_to_ten(expect,ans):
                try:
                    a1=int(ans[0])
                    a2=int(ans[1])
                except ValueError:
                    a1=0
                    a2=0
                return (a1+a2)==int(expect)
        """),
    }
    status_indicators = {
        'correct': ['div.correct'],
        'incorrect': ['div.incorrect'],
        'unanswered': ['div.unanswered', 'div.unsubmitted'],
    }


    def answer_problem(self, correct):
        """
        Answer script problem.
        """
        # Correct answer is any two integers that sum to 10
        first_addend = random.randint(-100, 100)
        second_addend = 10 - first_addend

        # If we want an incorrect answer, then change
        # the second addend so they no longer sum to 10
        if not correct:
            second_addend += random.randint(1, 10)

        self.problem_page.fill_answer(first_addend, input_num=0)
        self.problem_page.fill_answer(second_addend, input_num=1)


class CodeProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'CODE TEST PROBLEM'
    problem_type = 'code'

    factory = CodeResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'Submit code to an external grader',
        'initial_display': 'print "Hello world!"',
        'grader_payload': '{"grader": "ps1/Spring2013/test_grader.py"}',
    }

    status_indicators = {
        'correct': ['.grader-status.correct'],
        'incorrect': ['.grader-status.incorrect'],
        'unanswered': ['.grader-status.unanswered'],
    }

    def answer_problem(self, correct):
        """
        Answer code problem.
        """
        # The fake xqueue server is configured to respond
        # correct / incorrect no matter what we submit.
        # Furthermore, since the inline code response uses
        # JavaScript to make the code display nicely, it's difficult
        # to programatically input text
        # (there's not <textarea> we can just fill text into)
        # For this reason, we submit the initial code in the response
        # (configured in the problem XML above)
        pass

class RadioTextProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'RADIO TEXT TEST PROBLEM'
    problem_type = 'radio_text'

    factory = ChoiceTextResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The correct answer is Choice 0 and input 8',
        'type': 'radiotextgroup',
        'choices': [
            ("true", {"answer": "8", "tolerance": "1"}),
            ("false", {"answer": "8", "tolerance": "1"}),
        ],
    }

    status_indicators = {
        'correct': ['section.choicetextgroup_correct'],
        'incorrect': ['section.choicetextgroup_incorrect', 'span.incorrect'],
        'unanswered': ['span.unanswered'],
    }

    def answer_problem(self, correct):
        """
        Answer radio text problem.
        """
        import ipdb; ipdb.set_trace()
        input_value = "8" if correct else "5"
        # self.problem_page.fill_answer(input_value)

        choice = "choiceinput_0bc" if correct else "choiceinput_1bc"
        # self.problem_page.click_choice(choice)


class CheckboxTextProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
    problem_name = 'CHECKBOX TEXT TEST PROBLEM'
    problem_type = 'checkbox_text'

    factory = ChoiceTextResponseXMLFactory()

    factory_kwargs = {
        'question_text': 'The correct answer is Choice 0 and input 8',
        'type': 'checkboxtextgroup',
        'choices': [
            ("true", {"answer": "8", "tolerance": "1"}),
            ("false", {"answer": "8", "tolerance": "1"}),
        ],
    }

    def answer_problem(self, correct):
        """
        Answer radio text problem.
        """
        input_value = "8" if correct else "5"
        # self.problem_page.fill_answer(input_value)

        choice = "choiceinput_0bc" if correct else "choiceinput_1bc"
        # self.problem_page.click_choice(choice)


# class ImageProblemTypeTest(ProblemTypeTest, ProblemTypeTestMixin):
#     problem_name = 'IMAGE TEST PROBLEM'
#     problem_type = 'image'

#     factory = ImageResponseXMLFactory()

#     factory_kwargs = {
#         'src': '/static/images/placeholder-image.png',
#         'rectangle': '(50,50)-(100,100)',
#     }

#     def answer_problem(self, correct):
#         """
#         Answer image problem.
#         """
#         offset = 25 if correct else -25

#         def try_click():
#             problem_html_loc = section_loc.course_key.make_usage_key('problem', 'image').html_id()
#             image_selector = "#imageinput_{}_2_1".format(problem_html_loc)
#             input_selector = "#input_{}_2_1".format(problem_html_loc)

#             world.browser.execute_script('$("body").on("click", function(event) {console.log(event);})')

#             initial_input = world.css_value(input_selector)
#             world.wait_for_visible(image_selector)
#             image = world.css_find(image_selector).first
#             (image.action_chains
#                 .move_to_element(image._element)
#                 .move_by_offset(offset, offset)
#                 .click()
#                 .perform())

#             world.wait_for(lambda _: world.css_value(input_selector) != initial_input)

#         world.retry_on_exception(try_click)





# TODO: ...

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can answer a problem incorrectly
    #     Given External graders respond "incorrect"
    #     And I am viewing a "<ProblemType>" problem
    #     When I answer a "<ProblemType>" problem "incorrectly"
    #     Then my "<ProblemType>" answer is marked "incorrect"
    #     And The "<ProblemType>" problem displays a "incorrect" answer
    #     """

    #     # Examples:
    #     # | ProblemType       |
    #     # | drop down         |
    #     # | multiple choice   |
    #     # | checkbox          |
    #     # | radio             |
    #     # #| string            |
    #     # | numerical         |
    #     # | formula           |
    #     # | script            |
    #     # | code              |
    #     # | radio_text        |
    #     # | checkbox_text     |
    #     # | image             |

    # def test_submit_blank_answer(self):
    #     """
    #     Scenario: I can submit a blank answer
    #     Given I am viewing a "<ProblemType>" problem
    #     When I check a problem
    #     Then my "<ProblemType>" answer is marked "incorrect"
    #     And The "<ProblemType>" problem displays a "blank" answer
    #     """

    #     # Examples:
    #     # | ProblemType       |
    #     # | drop down         |
    #     # | multiple choice   |
    #     # | checkbox          |
    #     # | radio             |
    #     # #| string            |
    #     # | numerical         |
    #     # | formula           |
    #     # | script            |
    #     # | radio_text        |
    #     # | checkbox_text     |
    #     # | image             |

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can reset a problem
    #     Given I am viewing a randomization "<Randomization>" "<ProblemType>" problem with reset button on
    #     And I answer a "<ProblemType>" problem "<Correctness>ly"
    #     When I reset the problem
    #     Then my "<ProblemType>" answer is marked "unanswered"
    #     And The "<ProblemType>" problem displays a "blank" answer
    #     """

    #     # Examples:
    #     # | ProblemType       | Correctness   | Randomization |
    #     # | drop down         | correct       | always        |
    #     # | drop down         | incorrect     | always        |
    #     # | multiple choice   | correct       | always        |
    #     # | multiple choice   | incorrect     | always        |
    #     # | checkbox          | correct       | always        |
    #     # | checkbox          | incorrect     | always        |
    #     # | radio             | correct       | always        |
    #     # | radio             | incorrect     | always        |
    #     # #| string            | correct       | always        |
    #     # #| string            | incorrect     | always        |
    #     # | numerical         | correct       | always        |
    #     # | numerical         | incorrect     | always        |
    #     # | formula           | correct       | always        |
    #     # | formula           | incorrect     | always        |
    #     # | script            | correct       | always        |
    #     # | script            | incorrect     | always        |
    #     # | radio_text        | correct       | always        |
    #     # | radio_text        | incorrect     | always        |
    #     # | checkbox_text     | correct       | always        |
    #     # | checkbox_text     | incorrect     | always        |
    #     # | image             | correct       | always        |
    #     # | image             | incorrect     | always        |

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can reset a non-randomized problem that I answer incorrectly
    #     Given I am viewing a randomization "<Randomization>" "<ProblemType>" problem with reset button on
    #     And I answer a "<ProblemType>" problem "<Correctness>ly"
    #     When I reset the problem
    #     Then my "<ProblemType>" answer is marked "unanswered"
    #     And The "<ProblemType>" problem displays a "blank" answer
    #     """

    #     # Examples:
    #     # | ProblemType       | Correctness   | Randomization   |
    #     # | drop down         | incorrect     | never           |
    #     # | multiple choice   | incorrect     | never           |
    #     # | checkbox          | incorrect     | never           |
    #     # # TE-572
    #     # #| radio             | incorrect     | never           |
    #     # #| string            | incorrect     | never           |
    #     # | numerical         | incorrect     | never           |
    #     # | formula           | incorrect     | never           |
    #     # # TE-572 failing intermittently
    #     # #| script            | incorrect     | never           |
    #     # | radio_text        | incorrect     | never           |
    #     # | checkbox_text     | incorrect     | never           |
    #     # | image             | incorrect     | never           |

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: The reset button doesn't show up
    #     Given I am viewing a randomization "<Randomization>" "<ProblemType>" problem with reset button on
    #     And I answer a "<ProblemType>" problem "<Correctness>ly"
    #     Then The "Reset" button does not appear
    #     """

    #     # Examples:
    #     # | ProblemType       | Correctness   | Randomization   |
    #     # | drop down         | correct       | never           |
    #     # | multiple choice   | correct       | never           |
    #     # | checkbox          | correct       | never           |
    #     # | radio             | correct       | never           |
    #     # #| string            | correct       | never           |
    #     # | numerical         | correct       | never           |
    #     # | formula           | correct       | never           |
    #     # | script            | correct       | never           |
    #     # | radio_text        | correct       | never           |
    #     # | checkbox_text     | correct       | never           |
    #     # | image             | correct       | never           |

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can answer a problem with one attempt correctly and not reset
    #     Given I am viewing a "multiple choice" problem with "1" attempt
    #     When I answer a "multiple choice" problem "correctly"
    #     Then The "Reset" button does not appear
    #     """

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can answer a problem with multiple attempts correctly and still reset the problem
    #     Given I am viewing a "multiple choice" problem with "3" attempts
    #     Then I should see "You have used 0 of 3 submissions" somewhere in the page
    #     When I answer a "multiple choice" problem "correctly"
    #     Then The "Reset" button does appear
    #     """

    #  def test_answer_incorrectly(self):
    #    """
    #     Scenario: I can answer a problem with multiple attempts correctly but cannot reset because randomization is off
    #     Given I am viewing a randomization "never" "multiple choice" problem with "3" attempts with reset
    #     Then I should see "You have used 0 of 3 submissions" somewhere in the page
    #     When I answer a "multiple choice" problem "correctly"
    #     Then The "Reset" button does not appear
    #     """

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can view how many attempts I have left on a problem
    #     Given I am viewing a "multiple choice" problem with "3" attempts
    #     Then I should see "You have used 0 of 3 submissions" somewhere in the page
    #     When I answer a "multiple choice" problem "incorrectly"
    #     And I reset the problem
    #     Then I should see "You have used 1 of 3 submissions" somewhere in the page
    #     When I answer a "multiple choice" problem "incorrectly"
    #     And I reset the problem
    #     Then I should see "You have used 2 of 3 submissions" somewhere in the page
    #     And The "Final Check" button does appear
    #     When I answer a "multiple choice" problem "correctly"
    #     Then The "Reset" button does not appear
    #     """

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can view and hide the answer if the problem has it:
    #     Given I am viewing a "numerical" that shows the answer "always"
    #     When I press the button with the label "SHOW ANSWER"
    #     Then the Show/Hide button label is "HIDE ANSWER"
    #     And I should see "4.14159" somewhere in the page
    #     When I press the button with the label "HIDE ANSWER"
    #     Then the Show/Hide button label is "SHOW ANSWER"
    #     And I should not see "4.14159" anywhere on the page
    #     """

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can see my score on a problem when I answer it and after I reset it
    #     Given I am viewing a "<ProblemType>" problem
    #     When I answer a "<ProblemType>" problem "<Correctness>ly"
    #     Then I should see a score of "<Score>"
    #     When I reset the problem
    #     Then I should see a score of "<Points Possible>"
    #     """

    #     # Examples:
    #     # | ProblemType       | Correctness   | Score               | Points Possible    |
    #     # | drop down         | correct       | 1/1 point           | 1 point possible   |
    #     # | drop down         | incorrect     | 1 point possible    | 1 point possible   |
    #     # | multiple choice   | correct       | 1/1 point           | 1 point possible   |
    #     # | multiple choice   | incorrect     | 1 point possible    | 1 point possible   |
    #     # | checkbox          | correct       | 1/1 point           | 1 point possible   |
    #     # | checkbox          | incorrect     | 1 point possible    | 1 point possible   |
    #     # | radio             | correct       | 1/1 point           | 1 point possible   |
    #     # | radio             | incorrect     | 1 point possible    | 1 point possible   |
    #     # #| string            | correct       | 1/1 point           | 1 point possible   |
    #     # #| string            | incorrect     | 1 point possible    | 1 point possible   |
    #     # | numerical         | correct       | 1/1 point           | 1 point possible   |
    #     # | numerical         | incorrect     | 1 point possible    | 1 point possible   |
    #     # | formula           | correct       | 1/1 point           | 1 point possible   |
    #     # | formula           | incorrect     | 1 point possible    | 1 point possible   |
    #     # | script            | correct       | 2/2 points          | 2 points possible  |
    #     # | script            | incorrect     | 2 points possible   | 2 points possible  |
    #     # | image             | correct       | 1/1 point           | 1 point possible   |
    #     # | image             | incorrect     | 1 point possible    | 1 point possible   |

    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can see my score on a problem when I answer it and after I reset it
    #     Given I am viewing a "<ProblemType>" problem with randomization "<Randomization>" with reset button on
    #     When I answer a "<ProblemType>" problem "<Correctness>ly"
    #     Then I should see a score of "<Score>"
    #     When I reset the problem
    #     Then I should see a score of "<Points Possible>"
    #     """

    #     # Examples:
    #     # | ProblemType       | Correctness   | Score               | Points Possible    | Randomization |
    #     # | drop down         | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | drop down         | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # | multiple choice   | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | multiple choice   | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # | checkbox          | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | checkbox          | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # | radio             | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | radio             | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # #| string            | correct       | 1/1 point           | 1 point possible   | never         |
    #     # #| string            | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # | numerical         | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | numerical         | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # | formula           | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | formula           | incorrect     | 1 point possible    | 1 point possible   | never         |
    #     # | script            | correct       | 2/2 points          | 2 points possible  | never         |
    #     # | script            | incorrect     | 2 points possible   | 2 points possible  | never         |
    #     # | image             | correct       | 1/1 point           | 1 point possible   | never         |
    #     # | image             | incorrect     | 1 point possible    | 1 point possible   | never         |


    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can see my score on a problem to which I submit a blank answer
    #     Given I am viewing a "<ProblemType>" problem
    #     When I check a problem
    #     Then I should see a score of "<Points Possible>"
    #     """

    #     # Examples:
    #     # | ProblemType       | Points Possible    |
    #     # | drop down         | 1 point possible   |
    #     # | multiple choice   | 1 point possible   |
    #     # | checkbox          | 1 point possible   |
    #     # | radio             | 1 point possible   |
    #     # #| string            | 1 point possible   |
    #     # | numerical         | 1 point possible   |
    #     # | formula           | 1 point possible   |
    #     # | script            | 2 points possible  |
    #     # | image             | 1 point possible   |


    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can reset the correctness of a problem after changing my answer
    #     Given I am viewing a "<ProblemType>" problem
    #     Then my "<ProblemType>" answer is marked "unanswered"
    #     When I answer a "<ProblemType>" problem "<InitialCorrectness>ly"
    #     And I input an answer on a "<ProblemType>" problem "<OtherCorrectness>ly"
    #     Then my "<ProblemType>" answer is marked "unanswered"
    #     And I reset the problem
    #     """

    #     # Examples:
    #     # | ProblemType     | InitialCorrectness | OtherCorrectness |
    #     # | drop down       | correct            | incorrect        |
    #     # | drop down       | incorrect          | correct          |
    #     # | checkbox        | correct            | incorrect        |
    #     # | checkbox        | incorrect          | correct          |
    #     # #| string          | correct            | incorrect        |
    #     # #| string          | incorrect          | correct          |
    #     # | numerical       | correct            | incorrect        |
    #     # | numerical       | incorrect          | correct          |
    #     # | formula         | correct            | incorrect        |
    #     # | formula         | incorrect          | correct          |
    #     # | script          | correct            | incorrect        |
    #     # | script          | incorrect          | correct          |

    # def test_answer_incorrectly(self):
    #     """
    #     Radio groups behave slightly differently than other types of checkboxes, because they
    #     don't put their status to the top left of the boxes (like checkboxes do), thus, they'll
    #     not ever have a status of "unanswered" once you've made an answer. They should simply NOT
    #     be marked either correct or incorrect. Arguably this behavior should be changed; when it
    #     is, these cases should move into the above Scenario.

    #     Scenario: I can reset the correctness of a radiogroup problem after changing my answer
    #     Given I am viewing a "<ProblemType>" problem
    #     When I answer a "<ProblemType>" problem "<InitialCorrectness>ly"
    #     Then my "<ProblemType>" answer is marked "<InitialCorrectness>"
    #     And I input an answer on a "<ProblemType>" problem "<OtherCorrectness>ly"
    #     Then my "<ProblemType>" answer is NOT marked "<InitialCorrectness>"
    #     And my "<ProblemType>" answer is NOT marked "<OtherCorrectness>"
    #     And I reset the problem
    #     """

    #     # Examples:
    #     # | ProblemType     | InitialCorrectness | OtherCorrectness |
    #     # | multiple choice | correct            | incorrect        |
    #     # | multiple choice | incorrect          | correct          |
    #     # | radio           | correct            | incorrect        |
    #     # | radio           | incorrect          | correct          |


    # def test_answer_incorrectly(self):
    #     """
    #     Scenario: I can reset the correctness of a problem after submitting a blank answer
    #     Given I am viewing a "<ProblemType>" problem
    #     When I check a problem
    #     And I input an answer on a "<ProblemType>" problem "correctly"
    #     Then my "<ProblemType>" answer is marked "unanswered"
    #     """

    #     # Examples:
    #     # | ProblemType       |
    #     # | drop down         |
    #     # | multiple choice   |
    #     # | checkbox          |
    #     # | radio             |
    #     # #| string            |
    #     # | numerical         |
    #     # | formula           |
    #     # | script            |
