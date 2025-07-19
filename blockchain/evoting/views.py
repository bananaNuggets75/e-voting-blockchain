from django.shortcuts import render, redirect
from django.db.models import F, Count
from .models import Voter, Candidate, Vote, Block
from django.utils import timezone
from .utils.blockchain import generate_hash 
import json

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

            # Prepare vote data for blockchain
            vote_data = {
                "voter": voter.name,
                "candidate": candidate.name,
                "party": candidate.party,
                "timestamp": vote.timestamp.isoformat()
            }

            # Convert vote data to JSON string
            vote_data_json = json.dumps(vote_data, sort_keys=True)

            # Generate block hash
            index = last_block.index + 1 if last_block else 1
            timestamp = timezone.now().isoformat()
            block_hash = generate_hash(index, vote_data_json, timestamp, previous_hash)

            # Create new block
            Block.objects.create(
                index=index,
                vote_data=vote_data_json,
                timestamp=timestamp,
                previous_hash=previous_hash,
                hash=block_hash
            )

            # Mark voter as voted
            voter.has_voted = True
            voter.save()

        return redirect('results')

    return render(request, 'vote.html', {'voters': voters, 'candidates': candidates})

def results(request):
    votes = Vote.objects.values(name=F('candidate__name')).annotate(total=Count('candidate'))
    return render(request, 'results.html', {'votes': votes})
