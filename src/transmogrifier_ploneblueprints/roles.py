# -*- coding: utf-8 -*-
from Acquisition import aq_base
from transmogrifier.blueprints import ConditionalBlueprint
from transmogrifier_ploneblueprints.utils import resolve_object
from venusianconfiguration import configure


@configure.transmogrifier.blueprint.component(name='plone.local_roles.get')
class GetLocalRoles(ConditionalBlueprint):
    def __iter__(self):
        context = self.transmogrifier.context
        for item in self.previous:
            if self.condition(item):
                obj = resolve_object(context, item)
                item['_block_inherit'] = getattr(aq_base(obj),
                                                 '__ac_local_roles_block__',
                                                 False)
                item['_local_roles'] = getattr(aq_base(obj),
                                               '__ac_local_roles__', {})
            yield item


@configure.transmogrifier.blueprint.component(name='plone.local_roles.set')
class SetLocalRoles(ConditionalBlueprint):
    def __iter__(self):
        context = self.transmogrifier.context
        for item in self.previous:
            if self.condition(item):
                obj = resolve_object(context, item)
                obj.__ac_local_roles__ = item['_local_roles']
                obj.__ac_local_roles_block__ = item['_block_inherit']
            yield item
