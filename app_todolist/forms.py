from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import *
from django.shortcuts import  get_object_or_404

class MappingTableForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=NewTodoList.objects.filter(active=True), required=False)
    destination = TreeNodeChoiceField(queryset=NewTodoList.objects.filter(active=True), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['parent'] = TreeNodeChoiceField(
            queryset=NewTodoList.objects.filter(active=True, author=user),
            label='Select a source',
            empty_label='--Select source --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select source--'

        self.fields['destination'] = TreeNodeChoiceField(
            queryset=NewTodoList.objects.filter(active=True, author=user),
            label='Select a destination',
            empty_label='--Select destination --'
        )
        self.fields['destination'].required = False
        self.fields['destination'].empty_label = '--Select destination--'

    def clean_source(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent.author != self.user:
            raise forms.ValidationError("You cannot set a source that belongs to another user.")
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    def clean_desitnation(self):
        parent = self.cleaned_data['destination']
        if parent is None:
            return None
        if parent.author != self.user:
            raise forms.ValidationError("You cannot set a destination that belongs to another user.")
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    class Meta:
        model = MappingTable
        fields = ['name', 'description', 'parent', 'destination' ]


### TYPELIST FORM
### TYPELIST is a separate model to store the types, so that we can refer
class TypeListForm(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=TypeList.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields['parent'] = TreeNodeChoiceField(
            queryset=TypeList.objects.filter(active=True, author=user),
            label='Select a source',
            empty_label='--Select source --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select source--'   

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent.author != self.user:
            raise forms.ValidationError("You cannot set a parent that belongs to another user.")
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
        
    class Meta:
        model = TypeList
        fields = ['parent', 'title','description' ]


class NewTodoListForm(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=NewTodoList.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, current_parent_id=None, *args, **kwargs):

        # begin separating the positional arguments for additional information
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = None

        super().__init__(data=data, *args, **kwargs)
        self.user = user
        self.current_parent_id = current_parent_id
        # end separating the positional arguments for additonal information

        # experiment with the selected workitem and mapped config relevant type 
        if current_parent_id:
            print(f">>>>> FORM {current_parent_id} <<<<<<")
            current_instance = NewTodoList.objects.get(active=True, author=user, id=current_parent_id)
            print(f">>>>>> FORM WORK ITEM TYPE ===== {current_instance.workitemtype} <<<<<<")
            if current_instance.workitemtype:
                mapping_details = TypeList.objects.get(active=True, author=user, id=current_instance.workitemtype.id)
                mapping_childrens = mapping_details.get_children()
                print(f">>>>FORM>>>{mapping_childrens}")
                self.fields['workitemtype'] = TreeNodeChoiceField(
                    queryset=mapping_childrens,
                    label='Select a Type',
                    empty_label='--Select type --'
                )
                self.fields['workitemtype'].required = False
                self.fields['workitemtype'].empty_label = '--Select type--'
            
        else:
            print("=================== no PARENT ID GIVEN for FORM ================")
            self.fields['workitemtype'] = TreeNodeChoiceField(
            queryset=TypeList.objects.filter(active=True, author=user),
            label='Select a Type',
            empty_label='--Select type --'
            )
            self.fields['workitemtype'].required = False
            self.fields['workitemtype'].empty_label = '--Select type--'
        

        self.fields['parent'] = TreeNodeChoiceField(
            queryset=NewTodoList.objects.filter(active=True, author=user),
            label='Select a parent',
            empty_label='--Select parent --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select parent--'

        

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent.author != self.user:
            raise forms.ValidationError("You cannot set a parent that belongs to another user.")
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    
    
    class Meta:
        model = NewTodoList
        fields = ['parent', 'title', 'workitemtype', 'description' ]


class EditNewTodoListForm(forms.ModelForm):
    details = None
    parent = TreeNodeChoiceField(queryset=NewTodoList.objects.filter(active=True), required=False)
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), required=False)

    def __init__(self, user, current_parent_id=None, *args, **kwargs):

        # begin separating the positional arguments for additional information
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data = None

        super().__init__(data=data, *args, **kwargs)
        self.user = user
        self.current_parent_id = current_parent_id
        # end separating the positional arguments for additonal information

        
        self.fields['workitemtype'] = TreeNodeChoiceField(
        queryset=TypeList.objects.filter(active=True, author=user),
        label='Select a Type',
        empty_label='--Select type --'
        )
        self.fields['workitemtype'].required = False
        self.fields['workitemtype'].empty_label = '--Select type--'
        

        self.fields['parent'] = TreeNodeChoiceField(
            queryset=NewTodoList.objects.filter(active=True, author=user),
            label='Select a parent',
            empty_label='--Select parent --'
        )
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = '--Select parent--'

        

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        if parent is None:
            return None
        if parent.author != self.user:
            raise forms.ValidationError("You cannot set a parent that belongs to another user.")
        if parent == self.instance:
            raise forms.ValidationError("A node may not be made a child of itself.")
        return parent
    
    
    class Meta:
        model = NewTodoList
        fields = ['parent', 'title', 'workitemtype', 'description' ]
