from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F, Count

from polls.models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    paginate_by = 10

    def get_queryset(self):
        """Return the last five published questions."""
        all_question = Question.objects.filter(pub_date__lte=timezone.now())

        if 'name' in self.request.GET:
            return all_question.order_by('text')

        if 'date' in self.request.GET:
            return all_question.order_by('pub_date')

        if 'vote' in self.request.GET:
            return all_question.annotate(Count('vote')).order_by('vote__count')

        return all_question.order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DeleteView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
