# Third Party Libraries
import pytest
from apistar.exceptions import TypeSystemError
from utils.schemas import EmailSchema, RegularText, formatted_date, regular_text


class TestRegularText:
    def test_space(self):
        RegularText('lijlijl okmok')

    params_test = ["jli#", "fzefzf*", "fzef\tfzef"]

    @pytest.mark.parametrize('mot', params_test)
    def test_unallowed(self, mot):
        with pytest.raises(TypeSystemError):
            RegularText(mot)

    def test_new_pattern(self):
        """
        text pattern modification in new
        """
        try:
            RegularText('zefzefzefzef####')
        except TypeSystemError as e:
            assert str(e) == RegularText.errors['pattern'].format(
                RegularText.pattern)

    def test_regular_text_function(self):
        a = regular_text(description="la description")
        b = a('le content')
        assert a.description == "la description"
        assert b == 'le content'


class TestDate:
    def test_new_pattern(self):
        """
        """
        try:
            formatted_date()('12-12-1925')
        except TypeSystemError as e:
            assert str(e) == formatted_date().errors['pattern'].format(
                formatted_date().pattern)


class TestEmail:
    def test_email_regex(self):
        """
        not exception should be raise.
        fixed :"-" in regex
        """
        a = [
            'hugues-garnier@rocher.fr',
            'gpERrre@letellier.fr',
            'imbe-rtan-dree@gregoire.fr',
            'ubonneau@perrier.org',
            'alain88@sfr.fr',
            'malletau_relie@dbmail.com',
            'chauvetrene@mon-nier.fr',
            'bouch-et_andre@thibault.org',
            'catherinemarchand@club-internet.fr',
            'mjulien@tiscali.fr',
        ]
        for i in a:
            EmailSchema(i)

    def test_email_unallowed(self):
        with pytest.raises(TypeSystemError):
            EmailSchema('fze#fze@fze.gt')
