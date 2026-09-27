<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const props = defineProps({ id: String })
const w = ref(null); const bayEnabled = ref(false); const bayDepth = ref(''); const msg = ref(''); const err = ref('')
onMounted(async () => {
  w.value = await getJSON(`/api/windows/${props.id}`)
  bayEnabled.value = !!w.value.bay_enabled
  bayDepth.value = w.value.bay_depth ?? ''
})
async function save() {
  msg.value = ''; err.value = ''
  try {
    const body = { bay_enabled: bayEnabled.value, bay_depth: bayDepth.value === '' ? null : Number(bayDepth.value) }
    w.value = await putJSON(`/api/windows/${props.id}/bay`, body)
    msg.value = '飘窗设置已保存'
  } catch (e) { err.value = '保存失败:' + e.message }
}
</script>
<template><div class="page" v-if="w"><h1>{{ w.name }}</h1><p v-if="w.data_quality==='dirty'" class="bad">{{ w.note }}</p><p>宽 {{ w.width }} 高 {{ w.height }} 褶倍 {{ w.fullness }}</p>
<div class="bay">
  <label><input type="checkbox" v-model="bayEnabled" /> 飘窗</label>
  <label>进深(米) <input type="number" step="0.01" min="0" v-model="bayDepth" placeholder="留空用默认" style="width:7em" /></label>
  <button @click="save">保存</button>
</div>
<p>当前:{{ w.bay_enabled ? `开,进深 ${w.bay_depth ?? '默认'}` : '关' }}</p>
<p v-if="msg">{{ msg }}</p><p v-if="err" class="bad">{{ err }}</p>
</div></template>
