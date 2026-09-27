<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { getJSON, postJSON, putJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const wid = ref(1); const fid = ref(1); const out = ref(null)
const bayEnabled = ref(false); const bayDepth = ref(''); const msg = ref(''); const err = ref('')
const cur = computed(() => windows.value.find(x => x.id === wid.value))
function syncBay() { bayEnabled.value = !!cur.value?.bay_enabled; bayDepth.value = cur.value?.bay_depth ?? ''; out.value = null }
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
  syncBay()
})
watch(wid, syncBay)
async function saveBay() {
  msg.value = ''; err.value = ''
  try {
    const body = { bay_enabled: bayEnabled.value, bay_depth: bayDepth.value === '' ? null : Number(bayDepth.value) }
    const w = await putJSON(`/api/windows/${wid.value}/bay`, body)
    const i = windows.value.findIndex(x => x.id === w.id); if (i >= 0) windows.value[i] = w
    msg.value = '飘窗设置已保存'
  } catch (e) { err.value = '飘窗保存失败:' + e.message }
}
async function go(save){
  msg.value = ''; err.value = ''
  try {
    out.value = save ? await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true}) : await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}`)
  } catch (e) { out.value = null; err.value = '测算被拒绝:' + e.message }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<div class="bay">
  <label><input type="checkbox" v-model="bayEnabled" /> 飘窗</label>
  <label>进深(米) <input type="number" step="0.01" min="0" v-model="bayDepth" placeholder="留空用默认" style="width:7em" /></label>
  <button @click="saveBay">保存飘窗</button>
</div>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="msg">{{ msg }}</p><p v-if="err" class="bad">{{ err }}</p>
<PanelCut v-if="out" :panels="out.panels" :cut-height="out.cut_height" :meters="out.meters" :bay-enabled="out.bay_enabled" :bay-depth="out.bay_depth" />
</div></template>
