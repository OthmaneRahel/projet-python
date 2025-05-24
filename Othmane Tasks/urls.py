path('question/<int:annonce_id>/', views.AjouterQuestion, name='questionadd'),
    path('reponse/<int:question_id>/<annonce_id>', views.repondreAuquestion.as_view(), name='reponseqst'),
    path('reponses/<int:question_id>/<annonce_id>', views.afficherResponse, name='reponsesqst'),