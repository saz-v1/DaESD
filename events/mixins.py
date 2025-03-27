from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from communities.models import Community, Membership

# Mixin to check if the user has permission to manage events for a community
# Saves us from repeating the same permission checks in multiple views
class EventPermissionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        # Try to get community from event (edit/delete views)
        # Create wont have an event object yet so we add an exception
        community = None
        try:
            event = self.get_object()
            community = event.community
        except AttributeError:
            # Create view fallback as no event object
            community_id = request.GET.get('community')
            if not community_id:
                return HttpResponseForbidden("No community specified.")
            try:
                community = Community.objects.get(pk=community_id)
            except Community.DoesNotExist:
                return HttpResponseForbidden("Community not found.")
            
        #  After obtaining object/community check if the user is authorized
        try:
            membership = Membership.objects.get(user=user, community=community)
            is_admin = membership.role == 'admin'
        except Membership.DoesNotExist:
            is_admin = False

        if not (user == community.creator or user.is_staff or is_admin):
            return HttpResponseForbidden("You do not have permission to manage events for this community.")

        return super().dispatch(request, *args, **kwargs)