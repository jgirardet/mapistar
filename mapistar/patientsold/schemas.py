from apistar import types, validators


class PatientSchema(types.Type):
    pk = validators.Integer(default=None)
    nom = validators.String(max_length=100)
    prenom = validators.String(max_length=100)
    ddn = validators.Date()
    # sexe = validators.Boolean(description="sexe", default=False)
    rue = validators.String(description="rue", default="")
    # postalcode: validators.Integer(description="Code Postal")
    # city: validators.String(description="Ville")
    # phonenumber: validators.String(description="Numéro de Téléphone")
    # email: validators.String(description="email")
    # alive: validators.Boolean(description="vivant ?")


class PatientUpdateSchema(PatientSchema):
    pk = validators.Integer(default=None)
    nom = validators.String(max_length=100, default='')
    prenom = validators.String(max_length=100, default=None)
    ddn = validators.Date(default='')
    # sexe = validators.Boolean(description="sexe", default=False)
    rue = validators.String(description="rue", default=None)


# class PatientWriteSchema(PatientSchema):
#     """"
#     PatientSchema with validation
#     enforce validated date at write time
#     """
#     updated_properties = {
#         'nom': regular_text(description="Nom"),
#         'firstname': regular_text(description="Prénom"),
#         'birthdate': formatted_date(description="Date de naissance"),
#         'email': email_schema(description="email"),
#     }
#     properties = dict(PatientSchema.properties, **updated_properties)
#     required = []

# class PatientCreateSchema(PatientWriteSchema):
#     """
#     Schema to create patients
#     """

#     properties = {
#         k: v
#         for k, v in PatientWriteSchema.properties.items()
#         if k not in ['id', 'alive']
#     }

#     required = [
#         'nom',
#         'prenom',
#         'ddn',
#     ]

# class PatientUpdateSchema(PatientWriteSchema):
#     """
#     schema to update patients
#     """
#     properties = {
#         k: v
#         for k, v in PatientSchema.properties.items() if k != 'id'
#     }

# required = []
