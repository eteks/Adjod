from django import forms
from banner.models import PostBanner

class PostBannertForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(PostBannertForm, self).__init__(*args, **kwargs)
		print "PostBannertForm", self.fields['bannerplan']
		# if "own" in self.fields['bannerplan']:
		# self.fields['link'].required = True
	   
	class Meta:
		model = PostBanner
		
