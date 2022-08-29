from django.shortcuts import render
from . import models
from rest_framework import generics
from .models import Document
from .serializers import DocumentSerializer
import os
import sqlite3
import openpyxl


def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        databasename1 = request.POST["fileTitle"] + 'exsel_database1.db'
        # Saving the information in the database
        document = models.Document(
            title=fileTitle,
            uploadedFile=uploadedFile,
            databasename1=databasename1
        )
        document.save()
        # метод sqlite3.connect автоматически создаст базу, если ее нет

        connect = sqlite3.connect(f'C:/Users/PopSmokePurpp/PycharmProjects/Django_B1/WebExsel/media/Uploaded Files/{fileTitle}exsel_datadase1.db')
        # курсор - это специальный объект, который делает запросы и получает результаты запросов
        cursor = connect.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS tab_1([_id] integer PRIMARY KEY AUTOINCREMENT,
            [bankacc] int,
            [saldo_vxod_aktiv] int,
            [saldo_vxod_pasiv] int,
            [oboroti_debet] int,
            [oboroti_kredit] int,
            [saldo_ishod_aktiv] int,
            [saldo_oshod_pasiv] int)
            ''')

        file_to_read = openpyxl.load_workbook(uploadedFile, data_only=True)
        sheet = file_to_read['Sheet1']
        for row in range(7, 636):
            # Объявление списка
            data = []
            # Цикл по столбцам от 1 до 4 ( 5 не включая)
            for col in range(1, 8):
                # value содержит значение ячейки с координатами row col
                value = sheet.cell(row, col).value
                # Список который мы потом будем добавлять
                data.append(value)

            # Вставка данных в поля таблицы
            cursor.execute(
                "INSERT INTO tab_1(bankacc, saldo_vxod_aktiv,"
                " saldo_vxod_pasiv, oboroti_debet, oboroti_kredit,"
                " saldo_ishod_aktiv, saldo_oshod_pasiv)"
                " VALUES (?, ?, ?, ?, ?, ?, ?);",
                (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

        # сохраняем изменения
        connect.commit()
        # закрытие соединения
        connect.close()

    documents = models.Document.objects.all()

    return render(request, "main/upload-file.html", context={
        "files": documents
    })


class DocumentAPIView(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
