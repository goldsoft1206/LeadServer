from django.core.management.base import NoArgsCommand

from leads.models import Lead, PointOfContact

class Command(NoArgsCommand):
    help = 'Cleans duplicate PoCs'

    def handle_noargs(self, **options):
        """ Remove any duplicate PoCs """
        print "Cleaning PoCs"
        
        for lead in Lead.objects.all():
            print "Checking lead:", lead
            pocs = {}
            pocsToDelete = []
            for poc in lead.pointofcontact_set.all():
                print "Checking poc:", poc
                print poc.street_address
                if poc.street_address in pocs:
                    pocsToDelete.append(poc)
                else:
                    pocs[poc.street_address] = poc
                    
            for poc in pocsToDelete:
                print "Deleteing poc:", poc
                poc.delete()