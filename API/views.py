import tensorflow as tf
from rest_framework import generics, mixins, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from API.models import Sentence, Student
from API.serializers import SentenceSerializer, NewSentenceSerializer, OtherSentenceSerializer
from tensorflow import keras
from .utilities import predict
from extra.my_diacritize import myDiacritize
from datetime import datetime

tf.config.list_physical_devices('GPU')

# Create your views here.
class SentenceList(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = SentenceSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('raw',)

    def get_queryset(self):
        queryset = Sentence.objects.all()
        diacritized = self.request.query_params.get('diacritized')
        if diacritized is not None:
            if (diacritized == "null"):
                diacritized = None
            queryset = queryset.filter(diacritized__exact=diacritized)
        return queryset.select_related('author')

    def get(self, request):
        return self.list(request)


class SentenceDetails(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
    lookup_field = 'id'

    def get(self, request, id):
        return self.retrieve(request, id=id)

    def put(self, request, id):
        request.data['diacritizer'] = self.request.user
        request.data['date_diacritized'] = datetime.now()
        return self.partial_update(request, id=id)

    def delete(self, request, id):
        return self.destroy(request, id=id)


class SentenceRequests(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Sentence.objects.filter(diacritized="")
    for i in queryset:
        grade=Student.objects.get(id=i.author.id).grade
        setattr(i, 'grade', grade)
    serializer_class = SentenceSerializer


    def get(self, request):
        return self.list(request)


class DiacritizationView(generics.GenericAPIView):
    serializer_class = NewSentenceSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data=request.data
        data['author'] = self.request.user
        serializer = OtherSentenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        DNN_input = serializer.validated_data['raw']
        model1 = keras.models.load_model('Encoder.sav')
        DNN_output =  predict(DNN_input, model1)
        # DNN_output2 = myDiacritize(DNN_input)
        # DNN_output3 = "DIACRITIZED SENTENCE"
        # if DNN_output2 == DNN_output1:
        #     serializer.validated_data['diacritized'] = DNN_output1
        # elif DNN_output3 == DNN_output1:
        #     serializer.validated_data['diacritized'] = DNN_output1
        # elif DNN_output3 == DNN_output2:
        #     serializer.validated_data['diacritized'] = DNN_output2
        # elif DNN_output2 == DNN_output3:
        #     serializer.validated_data['diacritized'] = DNN_output2
        # else:
        #     serializer.validated_data['diacritized'] = {DNN_output1, DNN_output2, DNN_output3}
        #     serializer.save()
        #     return Response({"Success": "Your request is pending, you will be notified when it is done."}, status=status.HTTP_201_CREATED)
        # serializer.save()
        # return Response(serializer.validated_data['diacritized'], status=status.HTTP_201_CREATED)
        serializer.validated_data['diacritized'] = DNN_output
        serializer.save()
        return Response(serializer.validated_data['diacritized'], status=status.HTTP_201_CREATED)


class DiacritizationFileView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def _processLine(self, request):
        print(request)
        data=request['data']
        data['author'] = self.request.user
        serializer = OtherSentenceSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        DNN_input = serializer.validated_data['raw']
        model = keras.models.load_model('Encoder.sav')
        '''
        DNN_output1 = "DIACRITIZED SENTENCE"
        DNN_output2 = "DIACRITIZED SENTENCE"
        DNN_output3 = "DIACRITIZED SENTENCE"
        if DNN_output2 == DNN_output1:
            serializer.validated_data['diacritized'] = DNN_output1
        elif DNN_output3 == DNN_output1:
            serializer.validated_data['diacritized'] = DNN_output1
        elif DNN_output3 == DNN_output2:
            serializer.validated_data['diacritized'] = DNN_output2
        elif DNN_output2 == DNN_output3:
            serializer.validated_data['diacritized'] = DNN_output2
        else:
            # serializer.validated_data['diacritized'] = {DNN_output1, DNN_output2, DNN_output3}
            serializer.save()
            return Response({"Success": "Your request is pending, you will be notified when it is done."}, status=status.HTTP_201_CREATED)
        serializer.save()
        return Response(serializer.validated_data['diacritized'], status=status.HTTP_201_CREATED)
        '''
        DNN_output = predict(DNN_input, model)
        serializer.validated_data['diacritized'] = DNN_output
        serializer.save()
        return serializer.data

    def post(self, request):
        decodedLines = request.FILES['file'].read().decode("utf8").split("\n")
        filteredDecodedLines = list(filter(lambda s: bool(s), decodedLines))
        print(filteredDecodedLines)
        responseList = []
        for line in filteredDecodedLines:
            responseList.append(self._processLine({
                'data': {
                    'raw': line
                } 
            }))
        return Response(responseList, status=status.HTTP_201_CREATED)