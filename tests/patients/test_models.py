# Standard Libraries
from string import capwords

# Third Party Libraries
import pytest
from patients.models import Patient

pytestmark = pytest.mark.django_db

# @pytest.mark.usefixtures('patientd')


class TestPatient:
    """
    Class to Test Patient model
    """

    attrs = ('name', 'firstname')

    def test_string(self, patientd):
        """
        test autoput of str
        """
        a = Patient.objects.create(**patientd)

        assert a.__str__() == a.firstname + ' ' + a.name

    def test_fields_with_capwords_at_create(self, patientd):
        """
        must be caps words :
            name
            firstname
        """
        attrs = self.attrs
        d = patientd
        for i in attrs:
            d[i] = d[i].lower()
        b = Patient.objects.create(**d)
        for i in attrs:
            assert getattr(b, i) == capwords(d[i])

    def test_fileds_with_capwords_at_update(self, patientd):
        b = Patient.objects.create(**patientd)
        for i in self.attrs:
            b.__dict__[i] = getattr(b, i).lower()
        b.save()
        for i in self.attrs:
            assert getattr(b, i) == capwords(patientd[i])

    def test_instance_update_capwords(self, patientd):
        b = Patient.objects.create(**patientd)
        a = "mkokmokmokmok"
        b.name = a
        b.save()
        assert b.name == capwords(a)

    def test_blank_true_for_non_required_fields(self, patientd):
        """
        mixer don't autopopulate blank fields
        """
        d = {i: patientd[i] for i in ['name', 'firstname', 'birthdate']}
        a = Patient(
            name=d['name'], firstname=d['firstname'], birthdate=d['birthdate'])
        a.save()
        b = Patient.objects.get(id=a.id)

        assert a == b
