import itertools
import pathlib
from textwrap import dedent

from truncatehtml import truncate




def _generate_status_badge_html(repo, github_url):
    return f"""
    <a class="reference external" href="{github_url}/actions/workflows/nightly-build.yaml"><img alt="nightly-build" src="{github_url}/actions/workflows/nightly-build.yaml/badge.svg" /></a>
    <a class="reference external" href="https://binder-staging.2i2c.cloud/v2/gh/ProjectPythiaTutorials/{repo}.git/main"><img alt="Binder" src="https://binder-staging.2i2c.cloud/badge_logo.svg" /></a>
    """

def _generate_sorted_tag_keys(all_items):

    key_set = set(itertools.chain(*[item['tags'].keys() for item in all_items]))
    return sorted(key_set)


def _generate_tag_set(all_items, tag_key=None):

    tag_set = set()
    for item in all_items:
        for k, e in item['tags'].items():
            if tag_key and k != tag_key:
                continue
            for t in e:
                tag_set.add(t)

    return tag_set


def _generate_tag_menu(all_items, tag_key):

    tag_set = _generate_tag_set(all_items, tag_key)
    tag_list = sorted(tag_set)

    options = ''.join(
        f'<li><label class="dropdown-item checkbox {tag_key}"><input type="checkbox" rel={tag.replace(" ", "-")} onchange="change();">&nbsp;{tag.capitalize()}</label></li>'
        for tag in tag_list
    )

    return f"""
<div class="dropdown">

<button class="btn btn-sm btn-outline-primary mx-1 dropdown-toggle" type="button" id="{tag_key}Dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
{tag_key.title()}
</button>
<ul class="dropdown-menu" aria-labelledby="{tag_key}Dropdown">
{options}
</ul>
</div>
"""


def generate_menu(all_items, submit_btn_txt=None, submit_btn_link=None):

    key_list = _generate_sorted_tag_keys(all_items)

    menu_html = '<div class="d-sm-flex mt-3 mb-4">\n'
    menu_html += '<div class="d-flex gallery-menu">\n'
    if submit_btn_txt:
        menu_html += f'<div><a role="button" class="btn btn-primary btn-sm mx-1" href={submit_btn_link}>{submit_btn_txt}</a></div>\n'
    menu_html += '</div>\n'
    menu_html += '<div class="ml-auto d-flex">\n'
    menu_html += '<div><button class="btn btn-link btn-sm mx-1" onclick="clearCbs()">Clear all filters</button></div>\n'
    for tag_key in key_list:
        menu_html += _generate_tag_menu(all_items, tag_key) + '\n'
    menu_html += '</div>\n'
    menu_html += '</div>\n'
    menu_html += '<script>$(document).on("click",function(){$(".collapse").collapse("hide");}); </script>\n'
    return menu_html


def build_from_items(items, filename, title='Gallery', subtitle=None, subtext=None, menu_html='', max_descr_len=300):

    # Build the gallery file
    panels_body = []
    for item in items:
        cookbook_url = item['url']
        status_badges = _generate_status_badge_html(item['repo'], item['github_url'])

        if not item.get('thumbnail'):
            item['thumbnail'] = '/_static/images/ebp-logo.png'
        thumbnail = item['thumbnail']

        tag_list = sorted((itertools.chain(*item['tags'].values())))
        tag_list_f = [tag.replace(' ', '-') for tag in tag_list]

        tags = [f'<span class="badge bg-primary mybadges">{tag}</span>' for tag in tag_list_f]
        tags = '\n'.join(tags)

        tag_class_str = ' '.join(tag_list_f)

        ellipsis_str = '<a class="modal-btn"> ... more</a>'
        short_description = truncate(item['description'], max_descr_len, ellipsis=ellipsis_str)

        if ellipsis_str in short_description:
            modal_str = f"""
<div class="modal">
<div class="content">
<img src="{thumbnail}" class="modal-img" />
<h3 class="display-3">{item["title"]}</h3>

<p class="my-2">{item['description']}</p>
<p class="my-2">{tags}</p>
<p class="mt-3 mb-0"><a href="{cookbook_url}" class="btn btn-outline-primary btn-block">Visit Website</a></p>
</div>
</div>
"""
        else:
            modal_str = ''

        panels_body.append(
            f"""\
---
:column: + tagged-card {tag_class_str}

<div class="d-flex gallery-card">
<img src="{thumbnail}" class="gallery-thumbnail" />
<div class="container">
<a href="{cookbook_url}" class="text-decoration-none"><h4 class="display-4 p-0">{item["title"]}</h4></a>
<p class="my-2">{short_description}</p>
</div>
</div>
{modal_str}

+++
<div class="tagsandbadges">
{tags}
<div{status_badges}</div>
</div>

"""
        )

    panels_body = '\n'.join(panels_body)

    stitle = f'#### {subtitle}' if subtitle else ''
    stext = subtext if subtext else ''

    panels = f"""
# {title}

{stitle}
{stext}

{menu_html}

````{{panels}}
:column: col-12
:card: +mb-4 w-100
:header: d-none
:body: p-3 m-0
:footer: p-1

{dedent(panels_body)}
````

<div class="modal-backdrop"></div>
<script src="/_static/custom.js"></script>
"""

    pathlib.Path(f'{filename}.md').write_text(panels)
    