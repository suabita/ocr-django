from django.utils.text import slugify


class SlugModelMixin(object):
    """" 
    Usado en los modelos donde hay slug.
    El método def get_slug obtiene el valor del slug según como se ha sobreescrito
    en el modelo.
    El método save asigna el valor obtenido en def get_slug al atributo slug
    en el modelo y lo guarda.
    """

    def get_slug(self):
        raise NotImplemented

    def save(self, *args, **kwargs):
        self.slug = slugify(self.get_slug())
        super(SlugModelMixin, self).save(*args, **kwargs)