from django.db import models
from django import forms
from django.shortcuts import render

from modelcluster.fields import ParentalKey, ParentalManyToManyField #parentalkey e manytomany legano una classe ad un altra, rendendola una figlia dell'altra
from modelcluster.contrib.taggit import ClusterTaggableManager #gestisce i tag
from taggit.models import TaggedItemBase #tag

from wagtail.wagtailcore.models import Page, Orderable #le classi child di orderable hanno un field sorted_by
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel #InlinePanel serve per infilare le immagini, Multipanel è figo
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet

@register_snippet #gestisce le categorie dei post
class PostCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(           #aggiunge un icona alle categorie
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    
    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categorie post'


class PostsIndexPage(Page):
    intro = RichTextField(blank=True)
    
    def get_context(self, request):
        #modifica il context originale per mostrare solo i post "pubblicati" ordinati in ordine cronologico 
        context = super(PostsIndexPage, self).get_context(request)
        postpages = self.get_children().live().order_by('-first_published_at')
        context['postpages'] = postpages
        return context

    def serve(self, request):
        postpages = self.get_children().live().order_by('-first_published_at')

        tag = request.GET.get('tag')
        if tag:
            postpages = postpages.filter(postpage__tags__name=tag)

        category = request.GET.get('category')
        if category:
            postpages = postpages.filter(postpage__categorie__name=category)

        editorial = self.get_children().live().order_by('-first_published_at').filter(
            postpage__categorie__name="Editoriale"
        ).first()

        return render(request, self.template, {
            'page': self,
            'postpages': postpages,
            'editorial': editorial,
        })

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname = 'full')
    ]
  
    subpage_types = ['PostPage']  #solo pagine del tipo dato sono creabili da questa classe

class PostPageTag(TaggedItemBase): 
    content_object = ParentalKey('Postpage', related_name='tagged_items') #parental key è come foreign key, lega i tag a PostPage, in più rende questa classe child di PostPage
    
class PostPage(Page): 
    data = models.DateTimeField('post data') #bisogna dargli dei limiti perchè per ora può essere messa nel passato e nel futuro 
    intro = models.CharField(max_length=300) #non so, lo lasciamo? è utile? 
    body = RichTextField(blank=True) #campo per il testo
    tags = ClusterTaggableManager(through=PostPageTag, blank=True) #aggiunge il campo tags 
    categorie = ParentalManyToManyField('posts.PostCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None


    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.SearchField('categorie'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(  #multifield è una figata, per ora ci ho messo sti 3 per leggibilità
            [  
            FieldPanel('data'),
            FieldPanel('tags'),
            FieldPanel('categorie', widget=forms.CheckboxSelectMultiple),
            ], 
        heading='Informazioni Post',
        classname='collapsible' #evita che siano sempre tutti visibili come lista di spunte
        ),    
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        InlinePanel('gallery_images', label='Galleria immagini'), #per images serve Inline o fa casino
        InlinePanel('related_links', label='Link correlati') #link utili
    ]

class PostPageRelatedLink(Orderable):
    page = ParentalKey(PostPage, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels =[
        FieldPanel('name'),
        FieldPanel('url'),
    ]

class PostPageGalleryImage(Orderable): #classe per le immagini dentro alle pagine Post
    page = ParentalKey(PostPage, related_name='gallery_images') #vedere sopra
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+' #models.CASCADE cancella l'entry nella gallery se la foto viene cancellata
    )
    descrizione = models.CharField(blank=True, max_length=250)

    panels =[
        ImageChooserPanel('image'),
        FieldPanel('descrizione'),
    ]

class PostTagIndexPage(Page): #definisce la view di tags

    def get_context(self, request):
        #filtra per tag
        tag = request.GET.get('tag')
        postpages = PostPage.objects.filter(tags__name=tag)

        #aggiorna il context nel template
        context = super(PostTagIndexPage, self).get_context(request)
        context['postpages'] = postpages
        return context
