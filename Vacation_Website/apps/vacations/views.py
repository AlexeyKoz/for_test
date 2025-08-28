# Views for vacation listing, details, creation, update, deletion, likes, and API endpoints.
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Vacation, Like
from apps.core.models import Country
from .serializers import VacationSerializer
from apps.core.serializers import CountrySerializer
from .forms import VacationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# ... existing code ...

# View for deleting a vacation directly (admin only).
@require_POST
def vacation_delete_direct(request, pk):
    # Only allow staff users to delete vacations
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    vacation = get_object_or_404(Vacation, pk=pk)
    vacation_name = vacation.country.name
    vacation.delete()
    
    return JsonResponse({
        'status': 'success', 
        'message': f'"{vacation_name}" was deleted successfully'
    })

# ... existing code ...

# Permission class to check if user is admin.
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

# View for the coming soon page.
class ComingSoonView(TemplateView):
    template_name = 'vacations/coming_soon.html'

# View for listing all vacations.
class VacationListView(ListView):
    model = Vacation
    template_name = 'vacations/vacation_list.html'
    context_object_name = 'vacations'
    ordering = ['-created_at']

    # Add is_liked flag to each vacation for the current user.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get all likes for the current user
            user_likes = set(Like.objects.filter(
                user=self.request.user
            ).values_list('vacation_id', flat=True))

            # Add is_liked flag to each vacation
            for vacation in context['vacations']:
                vacation.is_liked = vacation.id in user_likes
        return context

# View for vacation details.
class VacationDetailView(DetailView):
    model = Vacation
    template_name = 'vacations/vacation_detail.html'
    context_object_name = 'vacation'

    # Add is_liked flag for the current user.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacation = self.get_object()
        context['is_liked'] = False
        if self.request.user.is_authenticated:
            context['is_liked'] = vacation.is_liked_by(self.request.user)
        return context

# View for creating a new vacation (admin only).
class VacationCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vacation
    form_class = VacationForm
    template_name = 'vacations/vacation_form.html'
    success_url = reverse_lazy('vacations:vacation_list')

    # Only allow staff users to create vacations.
    def test_func(self):
        return self.request.user.is_staff

    # Show success message on valid form.
    def form_valid(self, form):
        messages.success(self.request, 'Vacation created successfully!')
        return super().form_valid(form)

# View for updating a vacation (admin only).
class VacationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vacation
    form_class = VacationForm
    template_name = 'vacations/vacation_form.html'
    success_url = reverse_lazy('vacations:vacation_list')

    # Only allow staff users to update vacations.
    def test_func(self):
        return self.request.user.is_staff

    # Show success message on valid form.
    def form_valid(self, form):
        messages.success(self.request, 'Vacation updated successfully!')
        return super().form_valid(form)

# View for deleting a vacation (admin only).
class VacationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vacation
    template_name = 'vacations/vacation_confirm_delete.html'
    success_url = reverse_lazy('vacations:vacation_list')

    # Only allow staff users to delete vacations.
    def test_func(self):
        return self.request.user.is_staff

    # Show success message on delete.
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Vacation deleted successfully!')
        return super().delete(request, *args, **kwargs)

# View for liking/unliking a vacation.
def vacation_like(request, pk):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Not authenticated'}, status=403)
        messages.warning(request, 'Please log in to like vacations.')
        return redirect('accounts:login')

    vacation = get_object_or_404(Vacation, pk=pk)
    like, created = Like.objects.get_or_create(
        user=request.user, vacation=vacation)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes_count': vacation.likes.count(),
        })
    return redirect('vacations:vacation_detail', pk=pk)

# API view for listing and creating vacations (admin only).
class VacationListAPIView(generics.ListCreateAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = [IsAdminUser]

# API view for retrieving, updating, and deleting a vacation (admin only).
class VacationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    permission_classes = [IsAdminUser]

# API view for liking a vacation (authenticated users).
class LikeVacationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Handle POST request to like a vacation.
    def post(self, request, pk):
        vacation = get_object_or_404(Vacation, pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user,
            vacation=vacation
        )

        if created:
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

# API view for unliking a vacation (authenticated users).
class UnlikeVacationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Handle DELETE request to unlike a vacation.
    def delete(self, request, pk):
        vacation = get_object_or_404(Vacation, pk=pk)
        try:
            like = Like.objects.get(user=request.user, vacation=vacation)
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_404_NOT_FOUND)

# API view for listing and creating countries.
class CountryListAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    # Set permissions for POST and GET requests.
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]
