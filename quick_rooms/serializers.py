

# class GuestBooking(models.Model):
#     room = models.ForeignKey(GuestHouseRoom, on_delete=models.CASCADE)
#     guest_house = models.ForeignKey(GuestHouse, on_delete=models.CASCADE)
#     campus = models.ForeignKey(CampusProfile, on_delete=models.PROTECT, null=True)
#     guest_user = models.ForeignKey(AnonymousGuest, on_delete=models.CASCADE)
#     booking_id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
#     start_time = models.DateTimeField(auto_now_add=True)
#     end_time = models.DateTimeField(null=True, blank=True)
#     status = models.CharField(max_length=20)
#     payed = models.BooleanField(default=False) 