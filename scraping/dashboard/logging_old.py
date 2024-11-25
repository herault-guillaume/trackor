with app.server.app_context():
    return html.Div(
        [
            dcc.Location(id="url", refresh=False),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            html.Img(
                                src="/assets/logo-bullion-sniper.webp",
                                style={"height": "150px", "width": "auto"},
                            )
                        ],
                        className="mb-4 mt-4",
                        justify="center",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.I(
                                                    className="fa-solid fa-user-plus",
                                                    style={"font-size": "18px"},
                                                ),
                                                "  S'inscrire",
                                            ],
                                            style={"text-align": "center"},
                                        ),
                                        dbc.CardBody(
                                            [
                                                # Email input with form feedback
                                                html.Div(
                                                    [
                                                        dbc.Input(
                                                            type="text",
                                                            id="signin-username-input",
                                                            placeholder="Entrez votre email",
                                                            valid=False,
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Format d'email invalide",
                                                            type="invalid",
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                                # Password input with form feedback
                                                html.Div(
                                                    [
                                                        dbc.Input(
                                                            type="password",
                                                            id="signin-password-input",
                                                            placeholder="Entrez votre mot de passe",
                                                            valid=False,
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Votre mot de passe doit faire 10 caractères",
                                                            type="invalid",
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                                # Confirm password input with form feedback
                                                html.Div(
                                                    [
                                                        dbc.Input(
                                                            type="password",
                                                            id="signin-confirm-password-input",
                                                            placeholder="Confirmez votre mot de passe",
                                                            valid=False,
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Les mots de passe ne correspondent pas.",
                                                            type="invalid",
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                                dbc.Button(
                                                    "Sign In",
                                                    id="signin-button",
                                                    color="secondary",
                                                    className="mr-2",
                                                ),
                                                html.Div(id="signin-output"),
                                            ]
                                        ),
                                    ],
                                    style={"text-align": "center"},
                                    className="mb-2",
                                ),
                                width=3,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.I(
                                                    className="fa-solid fa-right-to-bracket",
                                                    style={"font-size": "18px"},
                                                ),
                                                "  Se connecter",
                                            ],
                                            style={"text-align": "center"},
                                        ),
                                        dbc.CardBody(
                                            [
                                                # Email input with form feedback
                                                html.Div(
                                                    [
                                                        dbc.Input(
                                                            type="text",
                                                            id="login-username-input",
                                                            placeholder="Entrez votre email",
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Format d'email invalide",
                                                            type="invalid",
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                                # Password input with form feedback
                                                html.Div(
                                                    [
                                                        dbc.Input(
                                                            type="password",
                                                            id="login-password-input",
                                                            placeholder="Entrez votre mot de passe",
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Votre mot de passe contient minimum 10 caractères",
                                                            type="invalid",
                                                        ),
                                                    ],
                                                    className="mb-3",
                                                ),
                                                dbc.Button(
                                                    "Se connecter",
                                                    id="login-button",
                                                    color="secondary",
                                                    className="mr-2",
                                                ),
                                                html.Div(id="login-output"),
                                            ]
                                        ),
                                    ],
                                    style={"text-align": "center"},
                                    className="mb-2",
                                ),
                                width=3,
                            ),
                        ],
                        className="equal-height-cards",
                        justify="center",
                    ),
                ], id='page-content'
            ),
        ]
    )

# # Callback for signin username input
# @app.callback(
#     Output("signin-username-input", "valid"),
#     Output("signin-username-input", "invalid"),
#     Input("signin-username-input", "value"),
# )
# def validate_signin_username(username):
#     if username is None:
#         raise PreventUpdate
#     email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", username) is not None
#     return email_valid, not email_valid
#
# # Callback for signin password input
# @app.callback(
#     Output("signin-password-input", "valid"),
#     Output("signin-password-input", "invalid"),
#     Input("signin-password-input", "value"),
# )
# def validate_signin_password(password):
#     if password is None:
#         raise PreventUpdate
#     password_valid = len(password) >= 10 if password else False
#     return password_valid, not password_valid
#
# # Callback for signin confirm password input
# @app.callback(
#     Output("signin-confirm-password-input", "valid"),
#     Output("signin-confirm-password-input", "invalid"),
#     Input("signin-confirm-password-input", "value"),
#     State("signin-password-input", "value"),
# )
# def validate_signin_confirm_password(confirm_password, password):
#     if confirm_password is None:
#         raise PreventUpdate
#     confirm_password_valid = (
#         confirm_password == password if password and confirm_password else False
#     )
#     return confirm_password_valid, not confirm_password_valid
#
# # Callback for login username input
# @app.callback(
#     Output("login-username-input", "valid"),
#     Output("login-username-input", "invalid"),
#     Input("login-username-input", "value"),
# )
# def validate_login_username(username):
#     if username is None:
#         raise PreventUpdate
#     email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", username) is not None
#     return email_valid, not email_valid
#
#
# # Callback for login password input
# @app.callback(
#     Output("login-password-input", "valid"),
#     Output("login-password-input", "invalid"),
#     Input("login-password-input", "value"),
# )
# def validate_login_password(password):
#     if password is None:
#         raise PreventUpdate
#     password_valid = len(password) >= 10 if password else False
#     return password_valid, not password_valid

# # Callback for login button click (to handle database interaction)
# @app.callback(
#     Output("login-output", "children"),
#     Output("page-content", "children"),
#     Input("login-button", "n_clicks"),
#     State("login-username-input", "value"),
#     State("login-password-input", "value"),
#     State("login-username-input", "valid"),
#     State("login-password-input", "valid"),
# )
# def login_button_click(n_clicks, username, password, username_valid, password_valid):
#     if n_clicks is None:
#         raise PreventUpdate
#
#     if not all([username_valid, password_valid]):
#         return (
#             dbc.Alert(
#                 "Veuillez remplir correctement tous les champs.",
#                 id="alert-invalid-fields-login",
#                 is_open=True,
#                 dismissable=True,
#                 fade=True,
#                 color="dark",
#                 className="mt-4"
#             ),
#             dash.no_update,
#         )
#     session, tunnel = create_session()
#     user = User.get_user_by_username(session,username)
#     if user is None:  # Check if user exists before accessing username
#         return dbc.Alert("Identifiants invalides.", color="danger", is_open=True, dismissable=True, fade=True,
#                          className="mt-4"), dash.no_update
#     session.close()
#     tunnel.stop()
#
#     if user and check_password_hash(user.password, password):
#         login_user(user)
#
#         return dbc.Alert("Connecté !",
#                          color="success",
#                          is_open=True,
#                          dismissable=True,
#                          fade=True,
#                          className="mt-4"
#                          ), serve_layout()  # No alert on successful login
#     else:
#         return dbc.Alert("Identifiants invalides.",
#                          is_open=True,
#                          dismissable=True,
#                          fade=True,
#                          color="dark",
#                          className="mt-4"
#                          ), dash.no_update
#
#     session.close()
#
# Callback for signin button click
@app.callback(
    Output("signin-output", "children"),
    Input("signin-button", "n_clicks"),
    [State("signin-username-input", "value"),
     State("signin-password-input", "value"),
     State("signin-confirm-password-input", "value"),
     State("signin-username-input", "valid"),
     State("signin-password-input", "valid"),
     State("signin-confirm-password-input", "valid")],
)
def signin_button_click(n_clicks, username, password, confirm_password,
                        email_valid, password_valid, confirm_valid):
    with app.server.app_context():  # Access the app context
        csrf_token = session.get('_csrf_token', '')
        if n_clicks is None:
            return dash.no_update

        if not all([email_valid, password_valid, confirm_valid]):
            return dbc.Alert(
                "Veuillez remplir correctement tous les champs.",
                id="alert-invalid-fields",
                is_open=True,
                color="error",
            )

        try:
            # Check if user exists using Flask-Security's user_datastore
            existing_user = user_datastore.find_user(email=username)
            if existing_user:
                return html.Div([
                    dbc.Alert(
                        "Un utilisateur avec cet email existe déjà.",
                        id="alert-user-exists",
                        is_open=True,
                        dismissable=True,
                        fade=True,
                        color="dark",
                        className="mt-4"
                    )
                ])

            # Create an instance of your form (if you're using a custom form)
            form = ExtendedRegisterForm(
                email=username,
                password=password,
                password_confirm=confirm_password
            )

            if form.validate():
                # Create the user using Flask-Security's user_datastore
                new_user = user_datastore.create_user(
                    email=username.lower(),  # Use 'email' field, consistent with Flask-Security
                    password=hash_password(password),  # Use Flask-Security's hash_password
                    active=False
                )

                # Send confirmation email (using Flask-Security's functionality)
                confirmation_link, token = user_datastore.generate_confirmation_token(new_user)
                subject = "Confirm your email"
                html_body = render_template('email/activate.html', confirmation_link=confirmation_link)
                mail_util.send_mail(subject, new_user.email, html_body)

                return dbc.Alert(
                    [
                        html.P("Inscription réussie !"),
                        html.P("Un email de confirmation a été envoyé à votre adresse.")
                    ],
                    color="success",
                    is_open=True,
                    dismissable=True,
                    fade=True,
                    className="mt-4"
                )
            else:
                # Handle form errors
                error_messages = []
                for field, errors in form.errors.items():
                    for error in errors:
                        error_messages.append(f"{field}: {error}")
                return dbc.Alert(
                    error_messages,
                    color="danger",
                    is_open=True,
                    dismissable=True,
                    fade=True,
                    className="mt-4"
                )

        except BadRequest as e:  # Catch validation errors from Flask-Security
            return dbc.Alert(
                str(e),  # Display the error message from Flask-Security
                color="danger",
                is_open=True,
                dismissable=True,
                fade=True,
                className="mt-4"
            )
        except Exception as e:
            if session:
                session.rollback()
            logg.error(f"An error occurred: {e}")  # Log the error
            return dbc.Alert(
                f"Une erreur s'est produite: {e}",
                id="alert-inscription-error",
                is_open=True,
                dismissable=True,
                fade=True,
                color="danger",
                className="mt-4"
            )
