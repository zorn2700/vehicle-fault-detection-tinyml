#include "tinyml_model.h"
#include "model.cc"   // المصفوفة التي سيتم إنشاؤها لاحقاً

static TfLiteTensor* input_tensor = NULL;

void init_tinyml_model(void) {
    // سيتم استكمالها عند دمج TFLite Micro الفعلي
}

int run_inference(float32_t *features) {
    // هنا ستتم الاستدعاء الفعلي للنموذج
    // حاليًا نُرجع 0 للتجربة
    (void)features;
    return 0;
}
