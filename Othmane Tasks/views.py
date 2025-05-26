class repondreAuquestion(View):
    def get(self,request,question_id,annonce_id):
        question = Question.objects.get(id=question_id)
        annonce = get_object_or_404(Annonce, id=annonce_id)
        questions = Question.objects.filter(annonce_id=annonce_id)
        return render(request,"Utilisateur/detail_annonce.html",{"question_actif":question,'MEDIA_URL': settings.MEDIA_URL,"questions":questions,"annonce":annonce})
    def post(self,request,question_id,annonce_id):
        Reponses.objects.create(
            user_id=request.user.id,
            question_id=question_id,
            contenu = request.POST.get("contenu")
        )
        return redirect(f"/annonce/{annonce_id}")

def afficherResponse(request,question_id,annonce_id):
    question = Question.objects.get(id=question_id)
    annonce = get_object_or_404(Annonce, id=annonce_id)
    questions = Question.objects.filter(annonce_id=annonce_id)
    reponses = Reponses.objects.filter(question_id = question_id);

def AjouterQuestion(request,annonce_id):
    Question.objects.create(
        contenu = request.POST.get("contenu"),
        user_id = request.user.id,
        annonce_id = annonce_id
    )
    messages.success(request,"Commentaire ajouté")
    return redirect(f"/annonce/{annonce_id}")