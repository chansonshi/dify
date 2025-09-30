'use client'
import type { FC } from 'react'
import React, { useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import GenericTable from './generic-table'
import type { ColumnConfig, GenericTableRow } from './generic-table'
import type { WebhookParameter } from '../types'
import { createParameterTypeOptions, normalizeParameterType } from '../utils/parameter-type-utils'
import { VarType } from '@/app/components/workflow/types'

type ParameterTableProps = {
  title: string
  parameters: WebhookParameter[]
  onChange: (params: WebhookParameter[]) => void
  readonly?: boolean
  placeholder?: string
  contentType?: string
}

const ParameterTable: FC<ParameterTableProps> = ({
  title,
  parameters,
  onChange,
  readonly,
  placeholder,
  contentType,
}) => {
  const { t } = useTranslation()

  // Memoize typeOptions to prevent unnecessary re-renders that cause SimpleSelect state resets
  const typeOptions = useMemo(() =>
    createParameterTypeOptions(contentType),
  [contentType],
  )

  // Define columns based on component type - matching prototype design
  const columns: ColumnConfig[] = [
    {
      key: 'key',
      title: 'Variable Name',
      type: 'input',
      width: 'flex-1',
      placeholder: 'Variable Name',
    },
    {
      key: 'type',
      title: 'Type',
      type: 'select',
      width: 'w-[120px]',
      placeholder: 'Type',
      options: typeOptions,
    },
    {
      key: 'required',
      title: 'Required',
      type: 'switch',
      width: 'w-[88px]',
    },
  ]

  // Choose sensible default type for new rows according to content type
  const defaultTypeValue: VarType = typeOptions[0]?.value || 'string'

  // Empty row template for new rows
  const emptyRowData: GenericTableRow = {
    key: '',
    type: defaultTypeValue,
    required: false,
  }

  const tableData: GenericTableRow[] = parameters.map(param => ({
    key: param.name,
    type: param.type,
    required: param.required,
  }))

  const handleDataChange = (data: GenericTableRow[]) => {
    // For text/plain, enforce single text body semantics: keep only first non-empty row and force string type
    // For application/octet-stream, enforce single file body semantics: keep only first non-empty row and force file type
    const isTextPlain = (contentType || '').toLowerCase() === 'text/plain'
    const isOctetStream = (contentType || '').toLowerCase() === 'application/octet-stream'

    const normalized = data
      .filter(row => typeof row.key === 'string' && (row.key as string).trim() !== '')
      .map(row => ({
        name: String(row.key),
        type: isTextPlain ? VarType.string : isOctetStream ? VarType.file : normalizeParameterType((row.type as string)),
        required: Boolean(row.required),
      }))

    const newParams: WebhookParameter[] = (isTextPlain || isOctetStream)
      ? normalized.slice(0, 1)
      : normalized

    onChange(newParams)
  }

  return (
    <GenericTable
      title={title}
      columns={columns}
      data={tableData}
      onChange={handleDataChange}
      readonly={readonly}
      placeholder={placeholder || t('workflow.nodes.triggerWebhook.noParameters')}
      emptyRowData={emptyRowData}
      showHeader={true}
    />
  )
}

export default ParameterTable
