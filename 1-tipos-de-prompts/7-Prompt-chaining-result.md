# Prompt Chaining Result

> Saída real do `7-Prompt-channing.py` rodando no llama3.1 (~11 min), mantida como o modelo gerou.
> Os erros foram revisados contra a documentação do Ext JS 7 e estão marcados com `// ERRO:` no código e `> **ERRO:**` no texto.
>
> Resumo, ligado às limitações de Prompt Chaining:
> - **Propaga erro de uma etapa para as seguintes:** a regra "endDate >= startDate" se perdeu na etapa 1, não aparece no form da etapa 2, e mesmo assim o commit da etapa 3 diz que há validação.
> - **Depende de parsing correto:** a etapa 3 devia retornar só uma linha, mas veio com texto de introdução.
> - Além disso, o código da etapa 2 não roda: vários erros de API do Ext JS quebram a tela antes de qualquer interação útil.

## MODEL (Ext.data.Model)
```javascript
Ext.define('PromotionModel', {
    extend: 'Ext.data.Model',
    fields: [
        {
            name: 'id',
            type: 'int'
        },
        {
            name: 'description',
            type: 'string',
            validators: {
                type: 'presence'
            }
        },
        {
            name: 'startDate',
            type: 'date',
            validators: {
                type: 'presence'
            }
        },
        {
            name: 'endDate',
            type: 'date',
            validators: {
                type: 'presence',
                // ERRO: `dependent` não existe no validator `presence` (as opções dele são `message` e `allowEmpty`).
                // A regra "endDate >= startDate" da spec não foi implementada.
                // Ex. de correção: validators: ['presence', function (value, record) {
                //     return value >= record.get('startDate') || 'End date must be greater than or equal to start date';
                // }]
                dependent: 'startDate',
                // ERRO: a opção se chama `message`, não `msg`, então esta mensagem é ignorada.
                msg: 'End date must be greater than or equal to start date'
            }
        },
        {
            name: 'discount',
            type: 'float',
            validators: {
                type: 'range',
                min: 0,
                max: 100
            }
        },
        {
            name: 'active',
            type: 'boolean',
            defaultValue: true
        }
    ]
});
```

## VIEWS & CONTROLLER (Ext JS MVVM)
Here is the code for the CRUD screen in Ext JS 7 (classic toolkit) following the MVVM pattern:
```javascript
// Store
// ERRO: a store não tem `storeId` nem é registrada na Application (`stores: [...]`),
// então o `store: 'PromotionStore'` do grid não encontra nenhuma store e o grid fica sem dados.
// ERRO: a spec pede paginação, mas não há `pageSize` aqui nem `pagingtoolbar` no grid.
Ext.define('PromotionStore', {
    extend: 'Ext.data.Store',
    model: 'PromotionModel',
    autoLoad: true,
    proxy: {
        type: 'ajax',
        url: 'data/promotions.json',
        reader: {
            type: 'json'
        }
    }
});

// View
Ext.define('PromotionListView', {
    extend: 'Ext.grid.Panel',
    xtype: 'promotion-list',
    title: 'Promotions',
    store: 'PromotionStore',
    // ERRO: nenhuma coluna tem `text`, então o grid aparece sem cabeçalhos.
    columns: [
        // ERRO: o prompt pedia uma coluna por campo do model, mas a coluna `id` virou um `rownumberer`.
        {
            xtype: 'rownumberer',
            width: 50
        },
        {
            xtype: 'gridcolumn',
            dataIndex: 'description',
            flex: 1
        },
        {
            xtype: 'datecolumn',
            dataIndex: 'startDate',
            format: 'Y-m-d'
        },
        {
            xtype: 'datecolumn',
            dataIndex: 'endDate',
            format: 'Y-m-d'
        },
        {
            xtype: 'numbercolumn',
            dataIndex: 'discount',
            format: '0.00%'
        },
        {
            xtype: 'booleancolumn',
            dataIndex: 'active'
        }
    ],
    dockedItems: [
        {
            xtype: 'toolbar',
            dock: 'top',
            // ERRO: o prompt pedia filtros de coluna (plugin `gridfilters` + `filter` em cada coluna), não campos na toolbar.
            // ERRO: não existe botão "Novo", então o fluxo de criação do controller nunca é alcançado.
            items: [
                {
                    xtype: 'textfield',
                    emptyText: 'Filter by description',
                    listeners: {
                        change: function(field) {
                            // ERRO: neste listener `this` é o próprio textfield, que não tem getStore().
                            // Dá TypeError na primeira digitação (o mesmo vale para os dois datefields abaixo).
                            // Correto: field.up('grid').getStore().
                            this.getStore().filterBy(function(record) {
                                return record.get('description').toLowerCase().indexOf(field.getValue().toLowerCase()) !== -1;
                            });
                        }
                    }
                },
                {
                    xtype: 'datefield',
                    emptyText: 'Filter by start date',
                    listeners: {
                        change: function(field) {
                            this.getStore().filterBy(function(record) {
                                return record.get('startDate') >= field.getValue();
                            });
                        }
                    }
                },
                {
                    xtype: 'datefield',
                    emptyText: 'Filter by end date',
                    listeners: {
                        change: function(field) {
                            this.getStore().filterBy(function(record) {
                                return record.get('endDate') <= field.getValue();
                            });
                        }
                    }
                }
            ]
        }
    ]
});

// View Model
// ERRO: falta `alias: 'viewmodel.promotion'`, então o `viewModel: { type: 'promotion' }` do form não encontra esta classe.
Ext.define('PromotionViewModel', {
    extend: 'Ext.app.ViewModel',
    data: {
        selectedRecord: null
    },
    formulas: {
        // ERRO: a fórmula `isEditing` nunca é usada (não há nenhum `bind` nas views).
        isEditing: function(get) {
            return get('selectedRecord') !== null;
        }
    }
});

// View Controller
// ERRO: nenhuma view declara `controller: 'promotion'`, então este controller nunca é criado
// e os handlers em string dos botões ('onFormSave' etc.) não resolvem.
Ext.define('PromotionViewController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.promotion',
    control: {
        'promotion-list': {
            itemdblclick: 'onItemDblClick'
        }
    },
    onItemDblClick: function(grid, record) {
        this.getViewModel().set('selectedRecord', record);
        // ERRO: o form nunca recebe o registro (falta form.loadRecord(record) ou bind), então abre vazio na edição.
        // ERRO: setActiveItem com string procura id/itemId, mas 'promotion-form' é o xtype. Nenhum item tem esse itemId.
        this.getView().getLayout().setActiveItem('promotion-form');
    },
    // ERRO: o handler de um botão recebe (button, event), não (form, action), então `action.field.getValue()` dá TypeError.
    // Correto: pegar o form (ex.: button.up('form')) e usar form.updateRecord(record) ou form.getValues().
    onFormSave: function(form, action) {
        var record = this.getViewModel().get('selectedRecord');
        if (record) {
            record.set(action.field.getValue());
            // ERRO: sem `scope: this`, o `this` dentro de success/failure não é o controller e
            // this.getViewModel() quebra. Vale para todos os save/destroy abaixo.
            record.save({
                success: function(record, operation) {
                    this.getViewModel().set('selectedRecord', null);
                    this.getView().getLayout().setActiveItem('promotion-list');
                },
                failure: function(record, operation) {
                    Ext.Msg.alert('Error', 'Failed to save promotion');
                }
            });
        } else {
            var newRecord = Ext.create('PromotionModel', action.field.getValue());
            // ERRO: o registro novo não é adicionado à store, então não aparece no grid depois de salvar.
            newRecord.save({
                success: function(record, operation) {
                    // ERRO: depois de criar, a seleção deveria ser limpa (null), como no fluxo de edição.
                    this.getViewModel().set('selectedRecord', record);
                    this.getView().getLayout().setActiveItem('promotion-list');
                },
                failure: function(record, operation) {
                    Ext.Msg.alert('Error', 'Failed to save promotion');
                }
            });
        }
    },
    onFormCancel: function() {
        this.getViewModel().set('selectedRecord', null);
        this.getView().getLayout().setActiveItem('promotion-list');
    },
    onFormDelete: function() {
        var record = this.getViewModel().get('selectedRecord');
        if (record) {
            // ERRO: desde o Ext JS 5, excluir no servidor é record.erase(); destroy() só destrói o objeto em memória.
            record.destroy({
                success: function(record, operation) {
                    this.getViewModel().set('selectedRecord', null);
                    this.getView().getLayout().setActiveItem('promotion-list');
                },
                failure: function(record, operation) {
                    Ext.Msg.alert('Error', 'Failed to delete promotion');
                }
            });
        }
    }
});

// Form View
Ext.define('PromotionFormView', {
    extend: 'Ext.form.Panel',
    xtype: 'promotion-form',
    title: 'Promotion Form',
    viewModel: {
        type: 'promotion'
    },
    items: [
        {
            xtype: 'textfield',
            name: 'description',
            fieldLabel: 'Description',
            allowBlank: false
        },
        {
            xtype: 'datefield',
            name: 'startDate',
            fieldLabel: 'Start Date',
            allowBlank: false
        },
        {
            xtype: 'datefield',
            name: 'endDate',
            fieldLabel: 'End Date',
            // ERRO (propagado da etapa 1): nada impede data final menor que a inicial.
            // O model não tinha a regra, então a view também não tem.
            allowBlank: false
        },
        {
            xtype: 'numberfield',
            name: 'discount',
            fieldLabel: 'Discount',
            minValue: 0,
            maxValue: 100
        },
        {
            xtype: 'checkboxfield',
            name: 'active',
            fieldLabel: 'Active'
        }
    ],
    dockedItems: [
        {
            xtype: 'toolbar',
            dock: 'bottom',
            items: [
                {
                    xtype: 'button',
                    text: 'Save',
                    handler: 'onFormSave'
                },
                {
                    xtype: 'button',
                    text: 'Cancel',
                    handler: 'onFormCancel'
                },
                {
                    xtype: 'button',
                    text: 'Delete',
                    handler: 'onFormDelete'
                }
            ]
        }
    ]
});

// Main View
// ERRO: é aqui que deveria estar o `controller: 'promotion'`, e os itens do card precisam de `itemId` para o setActiveItem funcionar.
Ext.define('PromotionMainView', {
    extend: 'Ext.container.Container',
    xtype: 'promotion-main',
    layout: {
        type: 'card'
    },
    items: [
        {
            xtype: 'promotion-list'
        },
        {
            xtype: 'promotion-form'
        }
    ]
});
```
This code creates a CRUD screen with a list view and a form view. The list view displays a grid with columns for each field in the model, and includes filters for description, start date, and end date. The form view includes fields for each field in the model, and includes buttons for save, cancel, and delete. The view controller handles the save, cancel, and delete actions, and the view model stores the selected record and provides a formula for determining whether the form is in editing mode.

> **ERRO:** o resumo afirma que os filtros e as ações de salvar e excluir funcionam, mas todos quebram em runtime pelos erros apontados acima.

## COMMIT
Here is a single-line conventional commit message summarizing the new screen based on the model and views:

`feat: added CRUD screen for promotions with list and form views, implementing data binding and validation`

> **ERRO:** o prompt pedia só a mensagem em uma linha, mas veio uma frase de introdução e a mensagem entre crases. Se essa saída fosse usada direto (numa próxima etapa ou num `git commit -m`), a mensagem sairia errada. É a limitação "depende de parsing correto".
>
> **ERRO:** a mensagem afirma "data binding and validation", mas nenhum bind é usado e a validação de datas não existe. O erro das etapas anteriores chegou até o commit.

---
**Pipeline Model:** llama3.1 (all steps)
