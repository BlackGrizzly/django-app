import csv
from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse

class ExportToCSVMixin:
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        field_names = [field.name for field in meta.fields]
        many_to_many_field_names = [many_to_many_field.name for many_to_many_field in meta.many_to_many]
		
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"

        csv_writer = csv.writer(response)
        csv_writer.writerow(field_names + many_to_many_field_names)      

        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            for field in many_to_many_field_names:
                row.append(','.join(map(str, getattr(obj, field).all().values_list('id', flat=True))))
            csv_writer.writerow(row)

        return response
    
    export_csv.short_description = "Экспорт в CSV"