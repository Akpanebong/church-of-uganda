from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from .utils import audit


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render


def model_form_view(request, model, form_class,
    template_name, success_url, pk=None, title="Record",):
    instance = get_object_or_404(model, pk=pk) if pk is not None else None
    is_update = instance is not None

    form = form_class(
        data=request.POST if request.method == "POST" else None,
        files=request.FILES if request.method == "POST" else None,
        instance=instance,
    )

    if request.method == "POST" and form.is_valid():
        obj = form.save()

        action = "updated" if is_update else "created"
        audit(
            request.user,
            action,
            obj,
            description=f"{title} {action} successfully.",
            request=request,
        )
        messages.success(
            request,
            f"{title} {action} successfully.",
        )

        if "<pk>" in success_url:
            return redirect(success_url.replace("<pk>", str(obj.pk)))

        return redirect(success_url)

    context = {
        "form": form,
        "object": instance,
        "page_title": f"{'Update' if is_update else 'Create'} {title}",
        "is_update": is_update,
    }

    return render(request, template_name, context)


@login_required
def model_delete_view(request, model, success_url, pk, title="Record", template_name="shared/confirm_delete.html"):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        try:
            obj.delete()
        except ProtectedError as exc:
            related_types = sorted({item.__class__.__name__ for item in exc.protected_objects})
            references = ", ".join(related_types) or "linked records"
            messages.error(
                request,
                f"{title} cannot be deleted because it is referenced by {references}. "
                "Deactivate the record instead, or resolve the linked leases, invoices and payments first.",
            )
            return redirect(success_url)
        audit(
            request.user,
            "deleted",
            obj,
            description=f"{title} deleted successfully.",
            request=request,
        )
        messages.success(request, f"{title} deleted successfully.")
        return redirect(success_url)
    return render(request, template_name,
                  {"object": obj, "page_title": f"Delete {title}", "cancel_url": success_url})
