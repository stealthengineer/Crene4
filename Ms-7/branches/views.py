from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.db.models import F, Count, Q,BooleanField,OuterRef,Subquery
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
import json
from .models import (Branch,
                    Leaf,
                    Politician,
                    Rating,
                    Topic)

from newshub.models import Voting

from .serializers import (BranchSerializer,
                          LeafSerializer,
                          PoliticianSerializer,
                          RatingSerializer,
                          TopicSerializer)


# Create your views here.
class AddBranch(APIView):
    def get(self, request):
        return render(request, "branch.html")


class BranchView(APIView):
    def get(self, request):
        topic=request.GET.get('topic')
        page_no=int(request.GET.get('page_no',1))
        topic_queryset = Topic.objects.all()
        serilized_topic = TopicSerializer(topic_queryset,many=True)
        query = Q(is_delete=False)
        if topic:
            query &= Q(topic=topic)
        voting_on_branch_filter = Voting.objects.filter(
                        branch=OuterRef('pk'),
                        user=request.user.id
                    )
        branches_queryset = Branch.objects.filter(query).annotate(
                fav_count = Count("votingonbranch__id",filter=Q(votingonbranch__in_favour = True)),
                unfav_count=Count("votingonbranch__id",filter=Q(votingonbranch__in_favour = False)),
                count_diff=F('fav_count')-F('unfav_count'),
                user_vote=Subquery(voting_on_branch_filter.values('in_favour')[:1],output_field=BooleanField()),
                                                ).order_by('-count_diff')
        p=Paginator(branches_queryset,15)
        if page_no <= p.num_pages:
            p_branches_queryset=p.page(page_no).object_list
            serilized_branches=BranchSerializer(p_branches_queryset,many=True)
            print(serilized_branches.data)
            if request.GET.get('datatype') == 'jsondata':
                return Response({'data':serilized_branches.data})
            return render(request,"branch.html",{'data':serilized_branches.data,'topics':serilized_topic.data})
        return Response({'data':'No data present'})
    
    def post(self, request):
        if request.user.is_authenticated:
            try:
                newbranch=Branch.objects.create(
                                            user_id=request.user.id,
                                            topic_id=request.POST.get('topic'),
                                            heading=request.POST.get('heading'),
                                            content=request.POST.get('content'),
                                            picture=request.FILES.get('picture'),
                                            is_delete=False
                                        )
                newbranch.save()
                # msg = 'Created Successfully'
                messages.success(request, 'Created Successfully')
                return HttpResponseRedirect(self.request.path_info)
            except Exception as e:
                messages.error(request, str(e))
            return HttpResponseRedirect(self.request.path_info)
        messages.error(request, 'Please login to create branch')
        return HttpResponseRedirect(self.request.path_info)
        
        
    
    def put(self,request):
        picture=request.POST.get('picture')
        branch_queryset=Branch.objects.get(id=request.POST.get('id'))
        if branch_queryset.user.id == request.user.id:
            branch_queryset.topic.id=request.POST.get('topic')
            branch_queryset.heading=request.POST.get('heading')
            branch_queryset.content=request.POST.get('content')
            if picture:
                branch_queryset.picture=picture
            branch_queryset.save()
            return Response({'msg':'Branch updated sucessfully'})
        return Response({'msg':'Unable to Update'})
            
    def delete(self,request):
        if request.user.is_authenticated:
            id = request.POST.get('id')
            branch_queyset= Branch.objects.get(id = id)
            if branch_queyset.user.id == request.user.id:
                branch_queyset.delete()
                return Response({'msg':'Deleted sucessfully'})
            return Response({'msg':'Unable to delete'})
        return Response({'msg':'You are not verified fot this action'})


class LeafView(APIView):
    def get(self,request):
        id = request.GET.get('id')
        if id:
            voting_on_leaf_filter = Voting.objects.filter(
                leaf=OuterRef('pk'),
                user=request.user.id)
            
            leaf_queryset = Leaf.objects.filter(parent_leaf = id
                                                ).annotate(
                fav_count = Count("votingonleaf__id",filter=Q(votingonleaf__in_favour = True)),
                unfav_count=Count("votingonleaf__id",filter=Q(votingonleaf__in_favour = False)),
                user_vote=Subquery(voting_on_leaf_filter.values('in_favour')[:1],output_field=BooleanField()),
                count_diff=F('fav_count')-F('unfav_count')
                                                ).order_by('-count_diff')
            serilized_leaves=LeafSerializer(leaf_queryset,many=True)
            return Response(
                {'data':serilized_leaves.data}
            )
        return Response({'msg':'getdemo'})
    
    def post(self,request):
        parent_leaf = request.POST.get('parent_leaf')
        is_parent = True if not parent_leaf else False
        try:
            newleaf = Leaf.objects.create(
                user_id = request.user.id,
                branch_id = request.POST.get('branch'),
                content = request.POST.get('content'),
                parent_leaf_id = parent_leaf,
                is_parent = is_parent
            )
            newleaf.save()
            return Response({'id':newleaf.id,'username':request.user.username})
        except Exception as e:
            msg = str(e)
        return Response({'msg':msg})
    
    def put(self,request):
        id = request.POST.get('id')
        user_id = request.user.id
        leaf_queyset = Leaf.objects.get(id = id)
        if leaf_queyset.user.id == user_id:
            leaf_queyset.content = request.POST.get('content')
            leaf_queyset.save()
            return Response({'msg':'Leaf updated Sucessfully'})
        return Response ({'msg':'Unable to update'})
    
    def delete(self,request):
        id = request.POST.get('id')
        leaf_queyset= Leaf.objects.get(id = id)
        if leaf_queyset.user.id == request.user.id:
            leaf_queyset.delete()
            return Response({'msg':'Deleted sucessfully'})
        return Response({'msg':'Unable to delete'})
    
    

class BranchDetail(APIView):
    def get(self,request,id):
        ordered = request.GET.get('sort','-count_diff')
        voting_on_branch_filter = Voting.objects.filter(
                branch=OuterRef('pk'),
                user=request.user.id
            )
        branch_queryset=Branch.objects.filter(id=id).annotate(
                fav_count = Count("votingonbranch__id",filter=Q(votingonbranch__in_favour = True)),
                unfav_count=Count("votingonbranch__id",filter=Q(votingonbranch__in_favour = False)),
                count_diff=F('fav_count')-F('unfav_count'),
                user_vote=Subquery(voting_on_branch_filter.values('in_favour')[:1],output_field=BooleanField()),
                                                ).order_by('-count_diff').get()
        serilized_branch=BranchSerializer(branch_queryset)
        query = Q(branch = id,is_parent = True)
        if request.GET.get('leaf'):
            query = Q(id=request.GET.get('leaf'))
        voting_on_leaf_filter = Voting.objects.filter(
                leaf=OuterRef('pk'),
                user=request.user.id
            )
        leaf_queryset = Leaf.objects.filter(query
                                                ).annotate(
                fav_count = Count("votingonleaf__in_favour",filter=Q(votingonleaf__in_favour = True)),
                unfav_count=Count("votingonleaf__id",filter=Q(votingonleaf__in_favour = False)),
                user_vote=Subquery(voting_on_leaf_filter.values('in_favour')[:1],output_field=BooleanField()),
                count_diff=F('fav_count')-F('unfav_count')
                                                ).order_by(ordered)
        serilized_leaves=LeafSerializer(leaf_queryset,many=True)
        serilized_topic = TopicSerializer(Topic.objects.all(),many=True)
        if request.GET.get('response_type') == 'json':
            json_leaves = json.dumps(serilized_leaves.data)
            print(json_leaves)
            return Response(json_leaves)
        return render(request,'branchdetail.html',{'branch':serilized_branch.data,'leaves':serilized_leaves.data,'topics':serilized_topic.data})
        return Response({'branch':serilized_branch.data,'leaves':serilized_leaves.data})
    

class RatePolitician(APIView):
    def get(self,request):
        id = request.GET.get('id')
        rating_queryset = Rating.objects.filter(politician = id)
        serilized_rating=RatingSerializer(rating_queryset,many=True)
        politician_queryset = Politician.objects.get(id = id)
        serilized_politician=PoliticianSerializer(politician_queryset)
        return Response({'politician':serilized_politician,'rating':serilized_rating})
    
    def post(self,request):
        id = request.POST.get('id')
        rate = request.POST.get('rate')
        feedback = request.POST.get('feedback')
        user_id = request.user.id
        try:
            obj = Rating.objects.create(
                user_id = user_id,
                politician_id = id,
                rate = rate,
                feedback = feedback
            )
            obj.save()
            msg = 'Submitted sucessfully'
        except Exception as e:
            msg = str(e)
        return Response({'msg':msg})
    
    def put(self,request):
        id = request.POST.get('id')
        user_id = request.user.id
        rating_queryset = Rating.objects.get(id = id)
        if rating_queryset.user.id == user_id:
            rating_queryset.rate = request.POST.get('rate')
            rating_queryset.feedback = request.POST.get('feedback')
            rating_queryset.save()
            return Response({'msg':'Updated Sucessfully'})
        return Response({'msg':'Unable to Update'})
            
    def delete(self,request):
        id = request.POST.get('id')
        rating_queryset = Rating.objects.get(id = id)
        if rating_queryset.user.id == request.user.id:
            rating_queryset.delete()
            return Response({'msg':'Deleted Sucessfully'})
    

class TopicListing(APIView):
    def get(self,request):
        return Response({'msg':'demo'})
    def post(self,request):
        if request.user.is_authenticated and request.POST.get('topic'):
            Topic.objects.create(
                
            )




# class HomePolitician(APIView):
#     def get(self,request):
#         politician_queryset = Politician.objects.all().annotate(
#                                                                 rating = Sum('politicianrating__rate'),
#                                                                 total_rating = Count('politicianrating')
#                                                                 )
#         serilized_politician=HomePoliticianSerializer(politician_queryset ,many=True)

#         return Response({'politician':serilized_politician})







    

    


    




