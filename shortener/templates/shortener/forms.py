from django import forms

class SubmitURLForm(forms.Form):
	url = forms.CharField(label='Submit URL')

	def clean(self):
		cleaned_data = super(SubmitURLForm, self).clean()
		print("CL ", cleaned_data)