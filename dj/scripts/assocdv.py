#!/usr/bin/python

# creates cutlist items for dv files that might belong to an episode

import os

from process import process

from django.db.models import Q

from main.models import Client, Show, Location, Episode, Raw_File, Cut_List

class ass_dv(process):

    def one_dv(self, dv, seq ):
        # find Episodes this may be a part of, add a cutlist record
        eps = Episode.objects.filter(
            Q(start__lte=dv.end)|Q(start__isnull=True), 
            Q(end__gte=dv.start)|Q(end__isnull=True), 
            location=dv.location).exclude(slug='orphans' )
        if not eps:
            # if no episodes found, attach to the orphan bucket
            ep,created=Episode.objects.get_or_create(
               name='orphans',slug='orphans',
               location=dv.location)
            eps=[ep]
        for ep in eps:
            print ep
            cl, created = Cut_List.objects.get_or_create(
                episode=ep,
                raw_file=dv,
                sequence=seq)


    def one_loc(self,location):
      seq=0
      for dv in Raw_File.objects.filter(location=location).order_by('start'):
        seq+=1
        self.one_dv(dv,seq)

    def one_show(self, show):
      for loc in Location.objects.filter(show=show):
        print show,loc
        self.one_loc(loc)

if __name__=='__main__': 
    p=ass_dv()
    p.main()

