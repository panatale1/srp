from django import template

register = template.Library()

def paginator(context, adjacent_pages=2):
    start_page = max(context['page'].number - adjacent_pages, 1)
    if start_page < 3:
        start_page = 1
    end_page = context['page'].number + adjacent_pages + 1
    if end_page >= context['page'].paginator.num_pages - 1:
        end_page = context['page'].paginator.num_pages + 1
    page_numbers = [
        n for n in range(start_page, end_page) if 0 < n <= context['page'].paginator.num_pages]
    context.update({
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': context['page'].paginator.num_pages not in page_numbers,
        'pagination_url': context.get('pagination_url', '')
    })
    return context

register.inclusion_tag('summer_reading/includes/paginator.html', takes_context=True)(paginator)
