from django.shortcuts import render, redirect
from .models import Voter, Candidate, Vote, Block
from django.utils import timezone
from .utils.blockchain import generate_hash

def vote(request):
    voters = Voter.objects.filter(has_voted=False)
    candidates = Candidate.objects.all()

    if request.method == 'POST':
        voter_id = request.POST['voter']
        candidate_id = request.POST['candidate']
        voter = Voter.objects.get(id=voter_id)
        candidate = Candidate.objects.get(id=candidate_id)

        if not voter.has_voted:
            # Record vote
            vote = Vote.objects.create(voter=voter, candidate=candidate)

            # Get previous block hash
            last_block = Block.objects.order_by('-index').first()
            previous_hash = last_block.hash if last_block else "0"

            # Create block
            vote_data = {
                "voter": voter.name,
                "candidate": candidate.name,
                "party": candidate.party,
                "timestamp": vote.timestamp.isoformat()
            }

            block = Block.objects.create(
                index=last_block.index + 1 if last_block else 1,
                vote_data=vote_data,
                timestamp=timezone.now(),
                previous_hash=previous_hash,
                hash="temp"  # temporarily; will be overridden in save()
            )
            voter.has_voted = True
            voter.save()

        return redirect('results')

    return render(request, 'evoting/vote.html', {'voters': voters, 'candidates': candidates})
