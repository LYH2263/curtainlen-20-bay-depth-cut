<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const s = ref({}); const depth = ref(''); const msg = ref(''); const err = ref('')
onMounted(async () => { s.value = await getJSON('/api/settings'); depth.value = s.value.default_bay_depth ?? '' })
async function save() {
  msg.value = ''; err.value = ''
  try {
    await putJSON('/api/settings/default_bay_depth', { value: String(depth.value) })
    s.value = await getJSON('/api/settings')
    msg.value = '已保存,历史记录不受影响'
  } catch (e) { err.value = '保存失败:' + e.message }
}
</script>
<template><div class="page"><h1>设置</h1><p>默认褶倍 {{ s.default_fullness }}</p>
<p><label>默认飘窗进深(米) <input type="number" step="0.01" min="0" v-model="depth" style="width:7em" /></label> <button @click="save">保存</button></p>
<p v-if="msg">{{ msg }}</p><p v-if="err" class="bad">{{ err }}</p>
</div></template>
